# Placar com Pygame

## Sumário

1. [O que vamos construir?](#o-que-vamos-construir)
2. [Solicitando o nome do jogador](#solicitando-o-nome-do-jogador)
   - [Como funciona a entrada de texto no Pygame](#como-funciona-a-entrada-de-texto-no-pygame)
   - [Código da tela de entrada do nome](#código-da-tela-de-entrada-do-nome)
3. [Criando o placar](#criando-o-placar)
   - [Renderizando texto na tela](#renderizando-texto-na-tela)
   - [Código do placar](#código-do-placar)
4. [Aguardando cliques para atualizar o contador](#aguardando-cliques-para-atualizar-o-contador)
5. [Código completo comentado](#código-completo-comentado)
6. [Conceitos trabalhados](#conceitos-trabalhados)
7. [Desafios](#desafios)

---

## O que vamos construir?

Nesta aula vamos criar um programa Pygame que:

1. Abre uma **tela de entrada** onde o jogador digita seu nome.
2. Exibe uma **janela principal** com título personalizado.
3. Mostra um **placar no topo** da tela com o nome do jogador e um contador iniciado em zero.
4. A cada **clique do mouse** na janela, o contador do placar é incrementado em 1.

Ao final, o resultado terá esta aparência:

```
┌─────────────────────────────────────┐
│  Jogador: Ana          Pontos: 7    │  ← placar no topo
├─────────────────────────────────────┤
│                                     │
│          (área de jogo)             │
│                                     │
└─────────────────────────────────────┘
```

---

## Solicitando o nome do jogador

### Como funciona a entrada de texto no Pygame

O Pygame **não possui** uma função de entrada de texto pronta (como o `input()` do Python puro). Para coletar texto do teclado precisamos construir nossa própria lógica usando o sistema de **eventos**.

A ideia é a seguinte:

1. Criamos uma variável `nome` (string vazia no início) que acumulará as teclas pressionadas.
2. Mantemos um **laço de entrada** (`while coletando_nome`) separado do laço principal do jogo.
3. Dentro desse laço, capturamos eventos do tipo `pygame.KEYDOWN`:
   - Se a tecla for `K_RETURN` (Enter) **e** o nome não estiver vazio, saímos do laço.
   - Se a tecla for `K_BACKSPACE`, removemos o último caractere de `nome`.
   - Para qualquer outra tecla, usamos `evento.unicode` para obter o caractere correspondente e concatenamos em `nome`.
4. A cada frame, redesenhamos a tela mostrando o texto digitado até o momento, para que o jogador veja o que está escrevendo.

> 💡 **`evento.unicode`** é o atributo que contém a representação em texto do caractere pressionado, já levando em conta modificadores como Shift e Caps Lock. Por exemplo, ao pressionar `Shift + a`, `evento.unicode` retorna `"A"`.

> 💡 **`K_BACKSPACE`** e **`K_RETURN`** são constantes do Pygame que identificam as teclas Backspace e Enter, respectivamente. Todas as constantes de teclado começam com `K_` e podem ser consultadas na [documentação oficial](https://www.pygame.org/docs/ref/key.html).

### Código da tela de entrada do nome

```python
import pygame

pygame.init()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Placar Pygame")

# Cores
PRETO       = (0,   0,   0)
BRANCO      = (255, 255, 255)
CINZA_ESCURO = (30,  30,  30)
AMARELO     = (255, 220,  0)

# Fontes
fonte_titulo  = pygame.font.SysFont("Arial", 36, bold=True)
fonte_texto   = pygame.font.SysFont("Arial", 28)

# ── Tela de entrada do nome ──────────────────────────────────────────────────
nome = ""
coletando_nome = True

while coletando_nome:
    tela.fill(CINZA_ESCURO)

    # Título da tela de entrada
    surf_titulo = fonte_titulo.render("Digite seu nome e pressione Enter:", True, BRANCO)
    tela.blit(surf_titulo, (LARGURA // 2 - surf_titulo.get_width() // 2, 220))

    # Exibe o texto digitado até o momento
    surf_nome = fonte_texto.render(nome + "|", True, AMARELO)   # "|" simula o cursor
    tela.blit(surf_nome, (LARGURA // 2 - surf_nome.get_width() // 2, 290))

    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN and nome.strip():
                coletando_nome = False          # Sai do laço ao pressionar Enter
            elif evento.key == pygame.K_BACKSPACE:
                nome = nome[:-1]                # Remove o último caractere
            else:
                nome += evento.unicode          # Acumula o caractere digitado
```

> **Detalhe importante:** `nome.strip()` verifica se a string não é composta apenas de espaços. Isso evita que o jogador avance com um nome em branco.

---

## Criando o placar

### Renderizando texto na tela

Para exibir texto no Pygame precisamos seguir três passos:

1. **Criar uma fonte** com `pygame.font.SysFont(nome_da_fonte, tamanho)`.
2. **Renderizar o texto** com `fonte.render(texto, antialias, cor)`, que retorna um objeto `Surface` com o texto desenhado.
3. **Copiar a Surface** para a tela com `tela.blit(superficie, (x, y))`.

```
fonte  = pygame.font.SysFont("Arial", 24)
surf   = fonte.render("Olá, Mundo!", True, (255, 255, 255))
tela.blit(surf, (10, 10))
```

> 💡 O segundo parâmetro de `render()` ativa o **antialiasing** (suavização das bordas do texto). Use `True` para textos maiores e `False` quando precisar de máxima performance.

### Código do placar

O placar é desenhado **a cada frame**, dentro do laço principal, antes de `pygame.display.flip()`. Isso garante que o contador atualizado seja exibido imediatamente após cada clique.

```python
def desenhar_placar(tela, nome, pontos, fonte, cor_fundo, cor_texto):
    """Desenha a faixa de placar no topo da janela."""
    # Retângulo de fundo do placar
    pygame.draw.rect(tela, cor_fundo, (0, 0, LARGURA, 50))

    # Texto com nome e pontuação
    texto = f"Jogador: {nome}          Pontos: {pontos}"
    surf  = fonte.render(texto, True, cor_texto)
    tela.blit(surf, (20, 13))
```

---

## Aguardando cliques para atualizar o contador

Após coletar o nome, entramos no **laço principal do jogo**. A cada iteração:

1. A tela é redesenhada (fundo + placar).
2. Os eventos são processados:
   - `pygame.QUIT` → encerra o programa.
   - `pygame.MOUSEBUTTONDOWN` com `evento.button == 1` → incrementa `pontos` em 1.

```python
pontos   = 0
rodando  = True

while rodando:
    tela.fill(COR_JOGO)
    desenhar_placar(tela, nome, pontos, fonte_placar, COR_PLACAR, BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pontos += 1     # Incrementa o contador a cada clique esquerdo

    pygame.display.flip()
```

---

## Código completo comentado

```python
import pygame

# ── 1. Inicialização ─────────────────────────────────────────────────────────
pygame.init()

LARGURA  = 800
ALTURA   = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Placar Pygame")

# ── 2. Cores ─────────────────────────────────────────────────────────────────
PRETO        = (0,   0,   0)
BRANCO       = (255, 255, 255)
CINZA_ESCURO = (30,  30,  30)
AMARELO      = (255, 220,  0)
AZUL_ESCURO  = (20,  40,  80)
AZUL_CLARO   = (40,  90, 160)

# ── 3. Fontes ─────────────────────────────────────────────────────────────────
fonte_titulo  = pygame.font.SysFont("Arial", 36, bold=True)
fonte_texto   = pygame.font.SysFont("Arial", 28)
fonte_placar  = pygame.font.SysFont("Arial", 24, bold=True)

# ── 4. Função auxiliar para o placar ─────────────────────────────────────────
def desenhar_placar(tela, nome, pontos):
    """Desenha a faixa de placar no topo da janela."""
    pygame.draw.rect(tela, AZUL_ESCURO, (0, 0, LARGURA, 50))     # Fundo do placar
    texto = f"Jogador: {nome}          Pontos: {pontos}"
    surf  = fonte_placar.render(texto, True, BRANCO)
    tela.blit(surf, (20, 13))

# ── 5. Tela de entrada do nome ───────────────────────────────────────────────
nome = ""
coletando_nome = True

while coletando_nome:
    tela.fill(CINZA_ESCURO)

    surf_instrucao = fonte_titulo.render("Digite seu nome e pressione Enter:", True, BRANCO)
    tela.blit(surf_instrucao, (LARGURA // 2 - surf_instrucao.get_width() // 2, 220))

    surf_nome = fonte_texto.render(nome + "|", True, AMARELO)
    tela.blit(surf_nome, (LARGURA // 2 - surf_nome.get_width() // 2, 290))

    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN and nome.strip():
                coletando_nome = False          # Confirma o nome e avança
            elif evento.key == pygame.K_BACKSPACE:
                nome = nome[:-1]                # Apaga o último caractere
            else:
                nome += evento.unicode          # Acumula o caractere digitado

# ── 6. Laço principal do jogo ────────────────────────────────────────────────
pontos  = 0
rodando = True

while rodando:
    # Preenche a área de jogo (abaixo do placar)
    tela.fill(AZUL_CLARO)

    # Desenha o placar no topo
    desenhar_placar(tela, nome, pontos)

    # Mensagem orientando o usuário
    surf_dica = fonte_texto.render("Clique na tela para pontuar!", True, BRANCO)
    tela.blit(surf_dica, (LARGURA // 2 - surf_dica.get_width() // 2, ALTURA // 2))

    # Processa os eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pontos += 1     # Incrementa o placar a cada clique esquerdo

    # Atualiza a janela
    pygame.display.flip()

# ── 7. Encerramento ──────────────────────────────────────────────────────────
pygame.quit()
print(f"Fim de jogo! {nome} fez {pontos} ponto(s).")
```

### O que acontece ao executar

1. Uma janela de 800 × 600 pixels abre em modo **entrada de nome**.
2. O jogador digita seu nome — cada tecla aparece na tela em tempo real; Backspace apaga o último caractere.
3. Ao pressionar **Enter**, o jogo começa: a janela exibe o **placar no topo** com nome e contador zerado.
4. Cada **clique esquerdo** na área de jogo incrementa o contador no placar.
5. Fechar a janela encerra o programa e imprime o resultado final no terminal.

---

## Conceitos trabalhados

| Conceito | Descrição |
|----------|-----------|
| **`pygame.font.SysFont`** | Cria uma fonte do sistema com nome e tamanho especificados, usada para renderizar texto na tela. |
| **`fonte.render()`** | Converte uma string em uma `Surface` (imagem de texto) pronta para ser copiada na janela. |
| **`tela.blit()`** | Copia uma `Surface` (imagem ou texto) para outra `Surface`, posicionando-a nas coordenadas informadas. |
| **`pygame.draw.rect()`** | Desenha um retângulo sólido ou vazado em uma `Surface`. Usado aqui como fundo do placar. |
| **`evento.type == KEYDOWN`** | Evento disparado quando qualquer tecla é pressionada. Permite capturar entradas do teclado. |
| **`evento.unicode`** | Atributo do evento `KEYDOWN` que contém o caractere gerado pela tecla, considerando modificadores (Shift, Caps Lock). |
| **`K_RETURN` / `K_BACKSPACE`** | Constantes do Pygame para identificar as teclas Enter e Backspace dentro de um evento `KEYDOWN`. |
| **`evento.button == 1`** | Filtra cliques do mouse para aceitar apenas o botão esquerdo (1 = esquerdo, 2 = meio, 3 = direito). |
| **Laço de entrada separado** | Padrão de usar um `while` dedicado antes do laço principal para coletar dados do usuário antes de iniciar o jogo. |
| **Função auxiliar** | Encapsular a lógica do placar em `desenhar_placar()` deixa o laço principal mais legível e o código reutilizável. |
| **`pygame.draw.rect()`** | Desenha retângulos coloridos na tela, útil para criar barras, botões e fundos de interface. |
| **Concatenação de string** | `nome += evento.unicode` acumula os caracteres digitados um a um para formar o nome completo. |
| **`str.strip()`** | Remove espaços em branco nas extremidades de uma string. Usado para validar que o nome não está vazio. |

---

## Desafios

### 🟢 Nível 1 — Fácil

1. **Mude as cores do placar:** experimente cores diferentes para o fundo e o texto do placar, como fundo verde-escuro e texto preto.
2. **Limite de caracteres:** impeça que o nome tenha mais de 15 caracteres. (Dica: só concatene `evento.unicode` se `len(nome) < 15`.)
3. **Mensagem de boas-vindas:** após confirmar o nome, exiba por 2 segundos uma mensagem `"Bem-vindo(a), <nome>!"` antes de entrar no laço principal. (Dica: use `pygame.time.delay(2000)`.)

### 🟡 Nível 2 — Intermediário

4. **Placar com nível:** exiba também um "Nível" no placar que sobe de 1 em 1 a cada 10 pontos. (Dica: `nivel = pontos // 10 + 1`.)
5. **Cor do placar muda conforme o nível:** altere a cor de fundo do placar dependendo do nível atual (por exemplo, verde para nível 1, amarelo para nível 2, vermelho para nível 3+).
6. **Botão direito remove ponto:** ao clicar com o botão direito (`evento.button == 3`) na área de jogo, diminua 1 ponto do placar, sem deixar o valor ficar negativo.

### 🔴 Nível 3 — Avançado

7. **Dois jogadores:** colete o nome de dois jogadores em sequência; cada jogador tem seu próprio placar. O botão esquerdo pontua para o jogador 1 e o botão direito para o jogador 2. Exiba os dois placar lado a lado no topo.
8. **Placar persistente em arquivo:** ao encerrar o jogo, salve `nome` e `pontos` em um arquivo `placar.txt`. Na próxima execução, leia o arquivo e exiba a pontuação anterior antes de começar.
9. **Temporizador regressivo:** adicione um cronômetro de 30 segundos no placar. Quando o tempo zerar, exiba uma tela de "Game Over" com a pontuação final e impeça novos cliques. (Dica: use `pygame.time.get_ticks()` para medir o tempo decorrido.)

---

> 📚 **Recursos úteis:**
> - Documentação oficial do Pygame: <https://www.pygame.org/docs/>
> - Módulo de fontes: <https://www.pygame.org/docs/ref/font.html>
> - Módulo de desenho: <https://www.pygame.org/docs/ref/draw.html>
> - Lista de constantes de teclado: <https://www.pygame.org/docs/ref/key.html>
> - Lista de eventos: <https://www.pygame.org/docs/ref/event.html>
