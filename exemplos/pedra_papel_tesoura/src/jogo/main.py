import pygame


LARGURA = 1000
ALTURA = 700
FPS = 60

FUNDO = (18, 25, 43)
PAINEL = (31, 42, 66)
PAINEL_CLARO = (43, 57, 86)
BRANCO = (245, 247, 255)
CINZA = (175, 186, 207)
VERDE = (56, 190, 130)
AZUL = (83, 145, 230)

OPCOES = ("Pedra", "Papel", "Tesoura")
DERROTA_PARA = {
    "Pedra": "Tesoura",
    "Papel": "Pedra",
    "Tesoura": "Papel",
}


def calcular_vencedor(jogada_1, jogada_2):
    """Retorna 0 ou 1 para o vencedor, ou -1 em caso de empate."""
    if jogada_1 == jogada_2:
        return -1
    if DERROTA_PARA[jogada_1] == jogada_2:
        return 0
    return 1


def desenhar_texto(tela, texto, fonte, cor, centro):
    imagem = fonte.render(texto, True, cor)
    retangulo = imagem.get_rect(center=centro)
    tela.blit(imagem, retangulo)


def desenhar_botao(tela, retangulo, texto, fonte, ativo=True, selecionado=False):
    if not ativo:
        cor = PAINEL_CLARO
    elif selecionado:
        cor = VERDE
    else:
        cor = AZUL

    pygame.draw.rect(tela, cor, retangulo, border_radius=10)
    desenhar_texto(tela, texto, fonte, BRANCO, retangulo.center)


def adicionar_jogador(nome, jogadores):
    nome = nome.strip()
    if not nome:
        return "Digite um nome antes de adicionar.", False
    if any(nome.casefold() == jogador.casefold() for jogador in jogadores):
        return "Esse nome já está na lista.", False
    jogadores.append(nome)
    return f"{nome} foi adicionado à lista.", True


def desenhar_tela_cadastro(
    tela,
    fontes,
    nome_digitado,
    jogadores,
    selecionados,
    inicio_lista,
    mensagem,
):
    fonte_titulo, fonte_subtitulo, fonte_texto, fonte_pequena = fontes
    tela.fill(FUNDO)

    desenhar_texto(tela, "Pedra, Papel e Tesoura", fonte_titulo, BRANCO, (500, 65))
    desenhar_texto(
        tela,
        "Cadastre os jogadores e selecione dois para começar",
        fonte_subtitulo,
        CINZA,
        (500, 120),
    )
    desenhar_texto(
        tela,
        "Nome do jogador",
        fonte_texto,
        BRANCO,
        (230, 160),
    )

    campo_nome = pygame.Rect(160, 178, 520, 54)
    botao_adicionar = pygame.Rect(700, 178, 140, 54)
    pygame.draw.rect(tela, PAINEL, campo_nome, border_radius=10)
    pygame.draw.rect(tela, AZUL, campo_nome, 2, border_radius=10)
    imagem_nome = fonte_texto.render(
        nome_digitado or "Digite aqui...",
        True,
        BRANCO if nome_digitado else CINZA,
    )
    tela.blit(imagem_nome, (campo_nome.x + 16, campo_nome.y + 13))
    desenhar_botao(tela, botao_adicionar, "Adicionar", fonte_texto)

    desenhar_texto(
        tela,
        f"Jogadores ({len(jogadores)}) - selecione 2",
        fonte_texto,
        BRANCO,
        (500, 258),
    )

    lista = pygame.Rect(160, 282, 680, 270)
    pygame.draw.rect(tela, PAINEL, lista, border_radius=12)
    tela.set_clip(lista)
    altura_linha = 48
    if not jogadores:
        desenhar_texto(
            tela,
            "Nenhum jogador adicionado ainda",
            fonte_pequena,
            CINZA,
            lista.center,
        )
    for indice in range(inicio_lista, min(inicio_lista + 5, len(jogadores))):
        y = lista.y + 8 + (indice - inicio_lista) * altura_linha
        linha = pygame.Rect(lista.x + 10, y, lista.width - 20, 40)
        escolhido = indice in selecionados
        pygame.draw.rect(
            tela,
            PAINEL_CLARO if escolhido else FUNDO,
            linha,
            border_radius=8,
        )
        if escolhido:
            ordem = selecionados.index(indice) + 1
            desenhar_texto(
                tela,
                f"J{ordem}",
                fonte_pequena,
                VERDE,
                (linha.x + 30, linha.centery),
            )
        desenhar_texto(
            tela,
            jogadores[indice],
            fonte_texto,
            BRANCO,
            (linha.x + 100, linha.centery),
        )
    tela.set_clip(None)

    if len(jogadores) > 5:
        desenhar_texto(
            tela,
            "Use a roda do mouse sobre a lista para navegar",
            fonte_pequena,
            CINZA,
            (500, 565),
        )
    if mensagem:
        desenhar_texto(tela, mensagem, fonte_pequena, CINZA, (500, 592))

    botao_iniciar = pygame.Rect(390, 625, 220, 54)
    desenhar_botao(
        tela,
        botao_iniciar,
        "Começar partida",
        fonte_texto,
        ativo=len(selecionados) == 2,
    )
    return botao_adicionar, lista, botao_iniciar


def retangulos_opcoes(cartao):
    largura = 118
    espacamento = 8
    inicio_x = cartao.x + (cartao.width - (largura * 3 + espacamento * 2)) // 2
    return [
        pygame.Rect(inicio_x + indice * (largura + espacamento), cartao.y + 235, largura, 52)
        for indice in range(3)
    ]


def desenhar_tela_jogo(tela, fontes, jogadores, escolhas, placar, rodada, resultado):
    fonte_titulo, fonte_subtitulo, fonte_texto, fonte_pequena = fontes
    tela.fill(FUNDO)

    botao_voltar = pygame.Rect(35, 28, 145, 44)
    desenhar_botao(tela, botao_voltar, "Voltar", fonte_pequena)
    desenhar_texto(tela, "Pedra, Papel e Tesoura", fonte_titulo, BRANCO, (500, 55))
    desenhar_texto(
        tela,
        f"Rodada {rodada}     {jogadores[0]}  {placar[0]} x {placar[1]}  {jogadores[1]}",
        fonte_subtitulo,
        CINZA,
        (500, 125),
    )

    cartoes = [pygame.Rect(55, 180, 425, 340), pygame.Rect(520, 180, 425, 340)]
    for indice, cartao in enumerate(cartoes):
        pygame.draw.rect(tela, PAINEL, cartao, border_radius=16)
        desenhar_texto(
            tela,
            jogadores[indice],
            fonte_subtitulo,
            BRANCO,
            (cartao.centerx, cartao.y + 48),
        )
        if escolhas[indice] is None:
            desenhar_texto(
                tela,
                "Escolha sua jogada",
                fonte_pequena,
                CINZA,
                (cartao.centerx, cartao.y + 115),
            )
            for opcao, retangulo in zip(OPCOES, retangulos_opcoes(cartao)):
                desenhar_botao(tela, retangulo, opcao, fonte_pequena)
        elif escolhas[1 - indice] is None:
            desenhar_texto(
                tela,
                "Jogada registrada!",
                fonte_subtitulo,
                VERDE,
                (cartao.centerx, cartao.y + 170),
            )
            desenhar_texto(
                tela,
                "Aguarde o outro jogador",
                fonte_pequena,
                CINZA,
                (cartao.centerx, cartao.y + 210),
            )
        else:
            desenhar_texto(
                tela,
                escolhas[indice].upper(),
                fonte_titulo,
                VERDE,
                (cartao.centerx, cartao.y + 175),
            )

    if resultado:
        desenhar_texto(tela, resultado, fonte_subtitulo, BRANCO, (500, 565))
        botao_proxima = pygame.Rect(370, 620, 260, 54)
        desenhar_botao(tela, botao_proxima, "Próxima rodada", fonte_texto)
    elif escolhas[0] is not None or escolhas[1] is not None:
        indice_aguardando = 0 if escolhas[0] is None else 1
        desenhar_texto(
            tela,
            f"Aguardando {jogadores[indice_aguardando]}...",
            fonte_texto,
            CINZA,
            (500, 565),
        )
        botao_proxima = None
    else:
        desenhar_texto(
            tela,
            "Cada jogador escolhe sua jogada. As escolhas aparecem juntas.",
            fonte_pequena,
            CINZA,
            (500, 565),
        )
        botao_proxima = None

    return botao_voltar, botao_proxima, cartoes


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Pedra, Papel e Tesoura")
    relogio = pygame.time.Clock()

    fontes = (
        pygame.font.Font(None, 48),
        pygame.font.Font(None, 30),
        pygame.font.Font(None, 24),
        pygame.font.Font(None, 20),
    )

    jogadores = []
    selecionados = []
    nome_digitado = ""
    mensagem = ""
    inicio_lista = 0
    tela_atual = "cadastro"

    jogadores_partida = []
    escolhas = [None, None]
    placar = [0, 0]
    rodada = 1
    resultado = ""

    pygame.key.start_text_input()
    executando = True
    while executando:
        if tela_atual == "cadastro":
            botao_adicionar, lista, botao_iniciar = desenhar_tela_cadastro(
                tela,
                fontes,
                nome_digitado,
                jogadores,
                selecionados,
                inicio_lista,
                mensagem,
            )
        else:
            botao_voltar, botao_proxima, cartoes = desenhar_tela_jogo(
                tela,
                fontes,
                jogadores_partida,
                escolhas,
                placar,
                rodada,
                resultado,
            )

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

            elif tela_atual == "cadastro":
                if evento.type == pygame.TEXTINPUT:
                    if len(nome_digitado) < 24:
                        nome_digitado += evento.text
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_BACKSPACE:
                        nome_digitado = nome_digitado[:-1]
                    elif evento.key == pygame.K_RETURN:
                        mensagem, adicionado = adicionar_jogador(nome_digitado, jogadores)
                        if adicionado:
                            nome_digitado = ""
                            inicio_lista = max(0, len(jogadores) - 5)
                elif evento.type == pygame.MOUSEWHEEL:
                    if lista.collidepoint(pygame.mouse.get_pos()):
                        inicio_lista -= evento.y
                        inicio_lista = max(0, min(inicio_lista, max(0, len(jogadores) - 5)))
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if botao_adicionar.collidepoint(evento.pos):
                        mensagem, adicionado = adicionar_jogador(nome_digitado, jogadores)
                        if adicionado:
                            nome_digitado = ""
                            inicio_lista = max(0, len(jogadores) - 5)
                    elif lista.collidepoint(evento.pos):
                        indice = inicio_lista + (evento.pos[1] - lista.y - 8) // 48
                        if 0 <= indice < len(jogadores) and (evento.pos[1] - lista.y - 8) % 48 < 40:
                            if indice in selecionados:
                                selecionados.remove(indice)
                                mensagem = "Jogador removido da seleção."
                            elif len(selecionados) < 2:
                                selecionados.append(indice)
                                mensagem = "Selecione mais um jogador." if len(selecionados) == 1 else "Dois jogadores selecionados."
                            else:
                                mensagem = "A partida permite selecionar apenas dois jogadores."
                    elif botao_iniciar.collidepoint(evento.pos) and len(selecionados) == 2:
                        jogadores_partida = [jogadores[indice] for indice in selecionados]
                        escolhas = [None, None]
                        placar = [0, 0]
                        rodada = 1
                        resultado = ""
                        tela_atual = "jogo"
                        break

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_voltar.collidepoint(evento.pos):
                    selecionados.clear()
                    mensagem = "Selecione dois jogadores para uma nova partida."
                    tela_atual = "cadastro"
                    break
                elif botao_proxima is not None and botao_proxima.collidepoint(evento.pos):
                    escolhas = [None, None]
                    resultado = ""
                    rodada += 1
                elif not resultado:
                    for indice, cartao in enumerate(cartoes):
                        if escolhas[indice] is None:
                            for opcao, retangulo in zip(OPCOES, retangulos_opcoes(cartao)):
                                if retangulo.collidepoint(evento.pos):
                                    escolhas[indice] = opcao
                                    if escolhas[0] is not None and escolhas[1] is not None:
                                        vencedor = calcular_vencedor(escolhas[0], escolhas[1])
                                        if vencedor == -1:
                                            resultado = "Empate! Ninguém marcou ponto."
                                        else:
                                            placar[vencedor] += 1
                                            resultado = f"{jogadores_partida[vencedor]} venceu a rodada!"
                                    break

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.key.stop_text_input()
    pygame.quit()


if __name__ == "__main__":
    main()