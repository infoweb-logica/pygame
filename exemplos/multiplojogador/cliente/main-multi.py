import asyncio
import json
import os
import queue
import random
import threading
import uuid

import pygame
import websockets
from dotenv import load_dotenv


load_dotenv()

# URL do servidor. Em outra máquina, substitua localhost pelo IP do servidor.
HOST = os.getenv("HOST", "127.0.0.1")
PORTA = os.getenv("PORT", "8765")
SERVIDOR_URL = f"ws://{HOST}:{PORTA}"


class Servidor:
    """
    Cliente WebSocket do jogo.

    A rede roda em uma thread/loop asyncio separado para não bloquear o loop
    principal do Pygame. As mensagens recebidas são colocadas em uma fila que
    Jogo consome na thread principal.
    """

    def __init__(self, jogo, url=SERVIDOR_URL):
        self.jogo = jogo
        self.url = url
        self.loop = None
        self.websocket = None
        self.thread = None
        self.fila_eventos = queue.Queue()
        self.conectado = threading.Event()
        self.inicializado = threading.Event()
        self._lock = threading.Lock()
        self._fechando = False

    def conectar(self, jogador):
        """Inicia a conexão em segundo plano e envia a mensagem 'entrar'."""
        self.jogador = jogador
        self.thread = threading.Thread(
            target=self._executar_loop, name="ClienteWebSocket", daemon=True
        )
        self.thread.start()

        # Aguarda a tentativa de conexão terminar, sem congelar indefinidamente.
        if not self.inicializado.wait(timeout=10):
            raise TimeoutError("Tempo esgotado ao conectar ao servidor.")

        if not self.conectado.is_set():
            erro = self.fila_eventos.get() if not self.fila_eventos.empty() else None
            detalhe = erro.get("mensagem", "Não foi possível conectar.") if erro else "Não foi possível conectar."
            raise ConnectionError(detalhe)

    def _executar_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._conectar_e_receber())

        if not self._fechando:
            self.loop.run_forever()

        # Encerra tarefas pendentes antes de fechar o loop.
        tarefas = asyncio.all_tasks(self.loop)
        for tarefa in tarefas:
            tarefa.cancel()
        if tarefas:
            self.loop.run_until_complete(
                asyncio.gather(*tarefas, return_exceptions=True)
            )
        self.loop.close()

    async def _conectar_e_receber(self):
        try:
            async with websockets.connect(self.url) as websocket:
                self.websocket = websocket

                await self._enviar({
                    "tipo": "entrar",
                    "id": str(self.jogador.id),
                    "nome": self.jogador.nome,
                    "posicao": list(self.jogador.posicao),
                })

                self.conectado.set()
                self.inicializado.set()

                async for mensagem in websocket:
                    try:
                        dados = json.loads(mensagem)
                        self.fila_eventos.put(dados)
                    except (json.JSONDecodeError, TypeError):
                        self.fila_eventos.put({
                            "tipo": "erro",
                            "mensagem": "O servidor enviou uma mensagem inválida."
                        })

        except Exception as erro:
            self.fila_eventos.put({
                "tipo": "erro",
                "mensagem": f"Falha na conexão com {self.url}: {erro}"
            })
        finally:
            self.conectado.clear()
            self.inicializado.set()
            self.websocket = None

    async def _enviar(self, dados):
        if self.websocket is not None:
            await self.websocket.send(json.dumps(dados))

    def mover(self, jogador):
        """Envia a posição atual do jogador local ao servidor."""
        if not self.conectado.is_set() or self.loop is None:
            return

        mensagem = {
            "tipo": "mover",
            "posicao": list(jogador.posicao),
        }
        asyncio.run_coroutine_threadsafe(self._enviar(mensagem), self.loop)

    def processar_eventos(self):
        """Retira da fila todas as atualizações de rede disponíveis."""
        while True:
            try:
                dados = self.fila_eventos.get_nowait()
            except queue.Empty:
                break

            tipo = dados.get("tipo")
            if tipo == "estado_inicial":
                # Recebe todos os jogadores existentes
                for jogador in dados.get("jogadores", []):
                    self.jogo.adicionar_jogador_remoto(jogador)
            elif tipo == "jogador_entrou":
                self.jogo.adicionar_jogador_remoto(dados)
            elif tipo == "jogador_moveu":
                self.jogo.mover_jogador_remoto(dados)
            elif tipo == "jogador_saiu":
                self.jogo.remover_jogador_remoto(dados.get("id"))
            elif tipo == "erro":
                print("Erro do servidor:", dados.get("mensagem", "Erro desconhecido"))

    def fechar(self):
        """Fecha a conexão; o servidor detectará a desconexão e avisará os demais."""
        self._fechando = True
        if self.loop and self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.close(), self.loop)
            self.loop.call_soon_threadsafe(self.loop.stop)
        elif self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)


class Jogador:
    def __init__(self, nome, cor=None, jogador_id=None):
        self.id = str(jogador_id or uuid.uuid4())
        self.nome = nome
        self.cor = cor or self.cor_aleatoria()
        self.posicao = (0, 0)
        self.janela = None
        self.tamanho = 20

    @classmethod
    def cor_aleatoria(cls):
        return tuple(random.randint(0, 255) for _ in range(3))

    @classmethod
    def posicao_aleatoria(cls, janela):
        largura = janela.get_width()
        altura = janela.get_height()
        return (
            random.randint(0, largura - 1),
            random.randint(0, altura - 1),
        )

    def desenhar(self):
        pygame.draw.circle(
            self.janela, self.cor,
            (int(self.posicao[0]), int(self.posicao[1])),
            self.tamanho // 2,
        )

    def andar(self, direcao):
        x, y = self.posicao
        largura = self.janela.get_width()
        altura = self.janela.get_height()
        passo = self.tamanho / 2

        if direcao == "cima":
            y = altura if y - self.tamanho < 0 else y - passo
        elif direcao == "baixo":
            y = 0 if y + self.tamanho > altura else y + passo
        elif direcao == "esquerda":
            x = largura if x - self.tamanho < 0 else x - passo
        elif direcao == "direita":
            x = 0 if x + self.tamanho > largura else x + passo

        self.posicao = (x, y)


class Jogo:
    def __init__(self):
        self.jogadores = {}  # ID -> Jogador
        self.jogador = None
        self.janela = None
        self.servidor = Servidor(self)

    def inicializar(self):
        pygame.init()
        pygame.display.set_caption("Jogo Multiplayer")
        self.janela = pygame.display.set_mode((800, 600))

    def adicionar_jogador(self, jogador):
        jogador.janela = self.janela
        jogador.posicao = Jogador.posicao_aleatoria(self.janela)
        self.jogador = jogador
        self.jogadores[jogador.id] = jogador

    def adicionar_jogador_remoto(self, dados):
        jogador_id = str(dados["id"])
        if jogador_id == self.jogador.id or jogador_id in self.jogadores:
            return

        jogador = Jogador(
            nome=dados.get("nome", "Jogador"),
            jogador_id=jogador_id,
        )
        jogador.janela = self.janela
        jogador.posicao = tuple(dados.get("posicao", (0, 0)))
        self.jogadores[jogador_id] = jogador
        print(f'{jogador.nome} entrou no jogo.')

    def mover_jogador_remoto(self, dados):
        jogador = self.jogadores.get(str(dados.get("id")))
        if jogador is not None:
            jogador.posicao = tuple(dados.get("posicao", jogador.posicao))

    def remover_jogador_remoto(self, jogador_id):
        if jogador_id is not None:
            jogador = self.jogadores.pop(str(jogador_id), None)
            if jogador:
                print(f"{jogador.nome} saiu do jogo.")

    def play(self):
        relogio = pygame.time.Clock()
        running = True

        try:
            while running:
                # Atualizações de rede são aplicadas na thread do Pygame.
                self.servidor.processar_eventos()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    elif event.type == pygame.KEYDOWN and self.jogador:
                        direcao = {
                            pygame.K_UP: "cima",
                            pygame.K_DOWN: "baixo",
                            pygame.K_LEFT: "esquerda",
                            pygame.K_RIGHT: "direita",
                        }.get(event.key)

                        if direcao:
                            self.jogador.andar(direcao)
                            self.servidor.mover(self.jogador)

                self.janela.fill((255, 255, 255))
                for jogador in self.jogadores.values():
                    jogador.desenhar()

                pygame.display.flip()
                relogio.tick(60)
        finally:
            self.servidor.fechar()
            pygame.quit()

    def start(self, jogador):
        self.inicializar()
        self.adicionar_jogador(jogador)
        try:
            self.servidor.conectar(jogador)
        except (ConnectionError, TimeoutError) as erro:
            print(f"Não foi possível entrar no jogo: {erro}")
            pygame.quit()
            return
        self.play()


if __name__ == "__main__":
    nome_jogador = input("Digite o nome do jogador: ").strip() or "Jogador"
    jogador = Jogador(nome_jogador)
    jogo = Jogo()
    jogo.start(jogador)
