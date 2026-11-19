import asyncio
import json
import websockets
import os
from dotenv import load_dotenv

# Configurações do servidor
load_dotenv()
HOST = os.getenv("HOST", "0.0.0.0")
PORTA = os.getenv("PORT", "8765")

# Lista de jogadores conectados
jogadores = {}

# Envia uma mensagem para um jogador
async def enviar_mensagem(conexao, mensagem):
    texto = json.dumps(mensagem)
    await conexao.send(texto)

# Envia uma mensagem para todos os jogadores,
# exceto para quem enviou a mensagem original
async def avisar_jogadores(mensagem, remetente=None):
    # print("=> notificando jogadores")
    for jogador in jogadores.values():
        # print(f"==> notificando {jogador['nome']}")
        conexao = jogador["conexao"]
        if conexao != remetente:
            await enviar_mensagem(conexao, mensagem)


# Controla a conexão de um jogador
async def conectar_jogador(conexao):
    id_jogador = None

    try:
        # Recebe os dados iniciais do jogador
        mensagem = await conexao.recv()
        dados = json.loads(mensagem)

        # Verifica se a mensagem é de entrada no jogo
        if dados["tipo"] != "entrar":
            return

        # Obtém os dados do jogador
        id_jogador = dados["id"]
        nome = dados["nome"]
        posicao = dados["posicao"]

        # Verifica se o jogador já está conectado
        if id_jogador in jogadores:
            await enviar_mensagem(conexao, {
                "tipo": "erro",
                "mensagem": "Jogador já conectado"
            })
            return

        # Guarda o jogador na lista
        jogadores[id_jogador] = {
            "nome": nome,
            "posicao": posicao,
            "conexao": conexao
        }

        # Envia o estado atual do jogo para o novo jogador
        lista_jogadores = []

        for id_existente, jogador_existente in jogadores.items():

            if id_existente == id_jogador:
                continue

            lista_jogadores.append({
                "id": id_existente,
                "nome": jogador_existente["nome"],
                "posicao": jogador_existente["posicao"]
            })

        await enviar_mensagem(conexao, {
            "tipo": "estado_inicial",
            "jogadores": lista_jogadores
        })

        print(nome, "entrou no jogo!")

        # Avisa os outros jogadores sobre a entrada
        await avisar_jogadores({
            "tipo": "jogador_entrou",
            "id": id_jogador,
            "nome": nome,
            "posicao": posicao
        }, conexao)

        # Recebe as mensagens enviadas pelo jogador
        async for mensagem in conexao:

            dados = json.loads(mensagem)

            # Verifica se o jogador quer atualizar sua posição
            if dados["tipo"] == "mover":

                # Obtém a nova posição
                nova_posicao = dados["posicao"]

                # Atualiza a posição do jogador
                jogadores[id_jogador]["posicao"] = nova_posicao

                print(nome, "moveu para", nova_posicao)

                # Avisa os outros jogadores sobre a movimentação
                await avisar_jogadores({
                    "tipo": "jogador_moveu",
                    "id": id_jogador,
                    "nome": nome,
                    "posicao": nova_posicao
                }, conexao)

    except websockets.exceptions.ConnectionClosed:
        print("Conexão encerrada.")

    finally:

        # Remove o jogador quando ele desconectar
        if id_jogador in jogadores:

            nome = jogadores[id_jogador]["nome"]

            del jogadores[id_jogador]

            print(nome, "saiu do jogo!")

            # Avisa os outros jogadores
            await avisar_jogadores({
                "tipo": "jogador_saiu",
                "id": id_jogador
            })


# Inicia o servidor
async def iniciar_servidor():

    print("Servidor iniciado!")
    print(f"Endereço: ws://{HOST}:{PORTA}")

    async with websockets.serve(
        conectar_jogador,
        HOST,
        PORTA
    ):
        await asyncio.Future()

if __name__ == "__main__":
    # Executa o programa
    asyncio.run(iniciar_servidor())
