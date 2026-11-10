import random
import pygame

class Jogador:
    def __init__(self, nome, cor):
        self.nome = nome
        self.cor = cor
        self.posicao = None
        self.janela = None
        self.tamanho = 20

    @classmethod
    def cor_aleatoria(cls):
        vermelho = random.randint(0, 255)
        verde = random.randint(0, 255)
        azul = random.randint(0, 255)
        return (vermelho, verde, azul)
    
    @classmethod
    def posicao_aleatoria(cls, janela):
        largura = janela.get_width()
        altura = janela.get_height()
        x = random.randint(0, largura)
        y = random.randint(0, altura)
        return (x, y)
    
    def desenhar(self):
        pygame.draw.circle(self.janela, self.cor, self.posicao, self.tamanho)

    def andar(self, direcao):
        if direcao == "cima":
            if self.posicao[1] - self.tamanho > 0:
                self.posicao = (self.posicao[0], self.janela.get_height() - 2)
            else:
                self.posicao = (self.posicao[0], self.posicao[1] - 10)
        elif direcao == "baixo":
            if self.posicao[1] + self.tamanho < self.janela.get_height():
                self.posicao = (self.posicao[0], 0)
            else:
                self.posicao = (self.posicao[0], self.posicao[1] + 10)
        elif direcao == "esquerda":
            if self.posicao[0] - self.tamanho > 0:
                self.posicao = (0, self.posicao[1])
            else:
                self.posicao = (self.posicao[0] - 10, self.posicao[1])
        elif direcao == "direita":
            if self.posicao[0] + self.tamanho < self.janela.get_width():
                self.posicao = (self.posicao[0] + 10, self.posicao[1])
            else:
                self.posicao = (self.janela.get_width() - 2, self.posicao[1])

class Jogo:
    def __init__(self):
        self.jogadores = []
        self.jogador = None
        self.janela = None
        self.servidor = None

    def inicializar(self):
        pygame.init()
        pygame.display.set_caption("Jogo Multiplayer")
        self.janela = pygame.display.set_mode((800, 600))

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.jogador.andar("cima")
                    elif event.key == pygame.K_DOWN:
                        self.jogador.andar("baixo")
                    elif event.key == pygame.K_LEFT:
                        self.jogador.andar("esquerda")
                    elif event.key == pygame.K_RIGHT:
                        self.jogador.andar("direita")
            self.janela.fill((255, 255, 255))
            if self.jogadores:
                for jogador in self.jogadores:
                    jogador.desenhar()
            pygame.display.flip()
        pygame.quit()

    def adicionar_jogador(self, jogador, externo=False):
        jogador.janela = self.janela
        self.jogadores.append(jogador)
        if not externo:
            jogador.posicao = Jogador.posicao_aleatoria(self.janela)
            self.jogador = jogador
    
    def start(self, jogador):
        self.inicializar()
        self.adicionar_jogador(jogador)
        self.play()

if __name__ == "__main__":
    nome_jogador = input("Digite o nome do jogador: ")
    jogador = Jogador(nome_jogador, Jogador.cor_aleatoria())
    jogo = Jogo()
    jogo.start(jogador)
