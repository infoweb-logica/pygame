# Mira, Tiro e Inimigo com Pygame

## Sumário

1. [O que vamos construir?](#o-que-vamos-construir)
2. [Parte 1 – Revisão: tela, nome e placar](#parte-1--revisão-tela-nome-e-placar)
   - [Revisando os conceitos](#revisando-os-conceitos)
   - [Código da Parte 1](#código-da-parte-1)
3. [Parte 2 – Mira e tiro com o mouse](#parte-2--mira-e-tiro-com-o-mouse)
   - [Escondendo o cursor padrão](#escondendo-o-cursor-padrão)
   - [Desenhando a mira](#desenhando-a-mira)
   - [Registrando o tiro](#registrando-o-tiro)
   - [Código da Parte 2](#código-da-parte-2)
   - [Conceitos da Parte 2](#conceitos-da-parte-2)
4. [Parte 3 – Inimigo em movimento aleatório](#parte-3--inimigo-em-movimento-aleatório)
   - [Criando o inimigo](#criando-o-inimigo)
   - [Movimento e rebatimento nas bordas](#movimento-e-rebatimento-nas-bordas)
   - [Código da Parte 3](#código-da-parte-3)
   - [Conceitos da Parte 3](#conceitos-da-parte-3)
5. [Parte 4 – Colisão e explosão](#parte-4--colisão-e-explosão)
   - [Verificando se o tiro acerta o inimigo](#verificando-se-o-tiro-acerta-o-inimigo)
   - [Animando a explosão](#animando-a-explosão)
   - [Código da Parte 4](#código-da-parte-4)
   - [Conceitos da Parte 4](#conceitos-da-parte-4)
6. [Código completo comentado](#código-completo-comentado)
7. [Conceitos trabalhados](#conceitos-trabalhados)
8. [Desafios](#desafios)

---

## O que vamos construir?

Neste tutorial vamos criar um **mini-jogo de tiro** com Pygame que:

1. Exibe uma tela de entrada para o nome do jogador e um **placar** no topo.
2. Substitui o cursor padrão por uma **mira de tiro** personalizada.
3. Ao clicar, mostra um **efeito de tiro** na posição clicada.
4. Gera um **inimigo** (quadrado vermelho) que se move aleatoriamente pela tela.
5. Quando o tiro acerta o inimigo, uma **explosão** é exibida, o inimigo reaparece em outro ponto e a pontuação aumenta.

```
┌──────────────────────────────────────────┐
│  Jogador: Ana             Pontos: 30     │  ← placar
├──────────────────────────────────────────┤
│                                          │
│        ╔════╗   ← inimigo               │
│        ║    ║                            │
│        ╚════╝                            │
│                                          │
│              ⊕  ← mira do mouse          │
│                                          │
└──────────────────────────────────────────┘
```

---

## Parte 1 – Revisão: tela, nome e placar

### Revisando os conceitos

No tutorial anterior ([02-pygame-placar.md](02-pygame-placar.md)) aprendemos a:

- Inicializar o Pygame e criar uma janela com `pygame.display.set_mode()` e `pygame.display.set_caption()`.
- Coletar o nome do jogador usando um **laço de entrada** separado com eventos `KEYDOWN`.
- Renderizar texto na tela com `pygame.font.SysFont` + `fonte.render()` + `tela.blit()`.
- Desenhar uma **faixa de placar** no topo com `pygame.draw.rect()`.

Nesta parte vamos apenas reutilizar esse código como base para os próximos passos.

### Código da Parte 1

```python
import pygame
import random

pygame.init()

LARGURA       = 800
ALTURA        = 600
ALTURA_PLACAR = 50         # Altura reservada para a faixa de placar

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Tiro – Pygame")

# ── Cores ────────────────────────────────────────────────────────────────────
PRETO        = (0,   0,   0)
BRANCO       = (255, 255, 255)
CINZA_ESCURO = (30,  30,  30)
AMARELO      = (255, 220,   0)
AZUL_ESCURO  = (20,  40,  80)
AZUL_CLARO   = (40,  90, 160)

# ── Fontes ───────────────────────────────────────────────────────────────────
fonte_titulo = pygame.font.SysFont("Arial", 36, bold=True)
fonte_texto  = pygame.font.SysFont("Arial", 28)
fonte_placar = pygame.font.SysFont("Arial", 24, bold=True)

# ── Função: desenhar placar ──────────────────────────────────────────────────
def desenhar_placar(tela, nome, pontos):
    pygame.draw.rect(tela, AZUL_ESCURO, (0, 0, LARGURA, ALTURA_PLACAR))
    texto = f"Jogador: {nome}          Pontos: {pontos}"
    surf  = fonte_placar.render(texto, True, BRANCO)
    tela.blit(surf, (20, 13))

# ── Laço de entrada do nome ──────────────────────────────────────────────────
nome = ""
coletando_nome = True

while coletando_nome:
    tela.fill(CINZA_ESCURO)
    surf_inst = fonte_titulo.render("Digite seu nome e pressione Enter:", True, BRANCO)
    tela.blit(surf_inst, (LARGURA // 2 - surf_inst.get_width() // 2, 220))
    surf_nome = fonte_texto.render(nome + "|", True, AMARELO)
    tela.blit(surf_nome, (LARGURA // 2 - surf_nome.get_width() // 2, 290))
    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN and nome.strip():
                coletando_nome = False
            elif evento.key == pygame.K_BACKSPACE:
                nome = nome[:-1]
            else:
                nome += evento.unicode

pontos  = 0
relogio = pygame.time.Clock()
```

> 🔁 Tudo que aparece aqui já foi explicado em detalhes no tutorial anterior. Caso tenha dúvidas, consulte o [02-pygame-placar.md](02-pygame-placar.md).

---

## Parte 2 – Mira e tiro com o mouse

Nesta parte vamos:

1. **Esconder o cursor padrão** do sistema operacional.
2. **Desenhar uma mira personalizada** na posição atual do mouse.
3. **Registrar um tiro** a cada clique e exibi-lo brevemente na tela.

### Escondendo o cursor padrão

Para substituir o cursor, primeiro precisamos tornar o cursor do sistema **invisível**:

```python
pygame.mouse.set_visible(False)
```

A partir desse momento, o Pygame não exibirá mais a seta padrão do sistema operacional. Nós mesmos cuidaremos de desenhar o cursor a cada frame.

### Desenhando a mira

A função `pygame.mouse.get_pos()` retorna a posição atual do cursor como uma tupla `(x, y)`. Com isso, desenhamos a mira **sempre atualizada** a cada frame:

```python
def desenhar_mira(tela, pos):
    """Desenha uma mira (crosshair) na posição dada."""
    x, y = pos
    COR_MIRA  = (220, 50, 50)  # Vermelho
    RAIO      = 12
    TAMANHO   = 18
    ESPESSURA = 2

    # Linhas cruzadas
    pygame.draw.line(tela, COR_MIRA, (x - TAMANHO, y), (x + TAMANHO, y), ESPESSURA)
    pygame.draw.line(tela, COR_MIRA, (x, y - TAMANHO), (x, y + TAMANHO), ESPESSURA)
    # Círculo central
    pygame.draw.circle(tela, COR_MIRA, (x, y), RAIO, ESPESSURA)
```

A mira é composta por:
- Duas **linhas** cruzadas (horizontal e vertical) centradas na posição do mouse.
- Um **círculo** ao redor do centro para facilitar a pontaria.

> 💡 **`pygame.draw.line(surface, cor, ponto_inicial, ponto_final, espessura)`** — desenha uma linha entre dois pontos. As coordenadas são tuplas `(x, y)`.

> 💡 **`pygame.draw.circle(surface, cor, centro, raio, espessura)`** — desenha um círculo. Se `espessura == 0`, o círculo é preenchido; se `espessura > 0`, apenas o contorno é desenhado.

### Registrando o tiro

Quando o jogador clica, queremos exibir um **flash de tiro** por alguns frames. Usamos uma variável de estado para isso:

```python
tiro = None  # None = nenhum tiro ativo
             # [x, y, frames_restantes] = tiro ativo
```

Ao detectar o clique:

```python
if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
    pos = pygame.mouse.get_pos()
    tiro = [pos[0], pos[1], 15]   # Tiro dura 15 frames
```

A cada frame, desenhamos e decrementamos o contador:

```python
if tiro:
    pygame.draw.circle(tela, AMARELO, (tiro[0], tiro[1]), 8)
    tiro[2] -= 1
    if tiro[2] <= 0:
        tiro = None
```

### Código da Parte 2

Adicione ao código da Parte 1 (logo antes do laço principal):

```python
pygame.mouse.set_visible(False)   # Esconde o cursor do sistema

tiro    = None   # [x, y, frames_restantes] ou None
rodando = True

while rodando:
    tela.fill(AZUL_CLARO)

    # Desenha o placar
    desenhar_placar(tela, nome, pontos)

    # Obtém a posição atual do mouse
    pos_mouse = pygame.mouse.get_pos()

    # Desenha o tiro (se ativo)
    if tiro:
        pygame.draw.circle(tela, AMARELO, (tiro[0], tiro[1]), 8)
        tiro[2] -= 1
        if tiro[2] <= 0:
            tiro = None

    # Desenha a mira por cima de tudo
    desenhar_mira(tela, pos_mouse)

    # Processa eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            tiro = [pos_mouse[0], pos_mouse[1], 15]

    pygame.display.flip()
    relogio.tick(60)   # Limita a 60 FPS

pygame.quit()
```

### Conceitos da Parte 2

| Conceito | Descrição |
|----------|-----------|
| **`pygame.mouse.set_visible(False)`** | Esconde o cursor padrão do sistema operacional para que possamos desenhar o nosso próprio cursor. |
| **`pygame.mouse.get_pos()`** | Retorna a posição atual do cursor como tupla `(x, y)` em pixels. |
| **`pygame.draw.line()`** | Desenha uma linha reta entre dois pontos com cor e espessura definidas. |
| **`pygame.draw.circle()`** | Desenha um círculo; com `espessura > 0` desenha apenas o contorno, com `espessura == 0` preenche. |
| **Variável de estado** | `tiro` pode ser `None` (sem tiro) ou uma lista com posição e contador de frames — padrão comum para gerenciar eventos temporários. |
| **`relogio.tick(60)`** | Limita a taxa de atualização a 60 FPS, controlando a velocidade do jogo. |

---

## Parte 3 – Inimigo em movimento aleatório

Nesta parte vamos criar um **inimigo** representado por um quadrado vermelho que:

- Aparece em uma **posição aleatória** na área de jogo.
- Move-se em uma **direção aleatória** a cada partida.
- **Rebate nas bordas** da tela, mantendo-se sempre visível.

### Criando o inimigo

Vamos usar o módulo `random` (já importado no início) para posicionar o inimigo:

```python
TAMANHO_INIMIGO = 40
VERMELHO        = (200, 40, 40)

inimigo_x = random.randint(0, LARGURA - TAMANHO_INIMIGO)
inimigo_y = random.randint(ALTURA_PLACAR, ALTURA - TAMANHO_INIMIGO)
```

> 💡 **`random.randint(a, b)`** retorna um número inteiro aleatório entre `a` e `b` (inclusive). Usamos `ALTURA_PLACAR` como mínimo para o eixo Y para garantir que o inimigo não apareça por baixo do placar.

O inimigo também precisa de uma **velocidade** — um vetor com componentes X e Y:

```python
vel_x = random.choice([-4, -3, -2, 2, 3, 4])
vel_y = random.choice([-4, -3, -2, 2, 3, 4])
```

> 💡 **`random.choice(sequencia)`** retorna um elemento escolhido aleatoriamente de uma sequência (lista, tupla, string). Excluímos o zero para que o inimigo sempre esteja em movimento.

### Movimento e rebatimento nas bordas

A cada frame, atualizamos a posição somando a velocidade:

```python
inimigo_x += vel_x
inimigo_y += vel_y
```

E verificamos se o inimigo saiu dos limites da tela — se saiu, **invertemos a velocidade** no eixo correspondente (efeito de rebote):

```python
if inimigo_x <= 0 or inimigo_x + TAMANHO_INIMIGO >= LARGURA:
    vel_x = -vel_x   # Inverte direção horizontal

if inimigo_y <= ALTURA_PLACAR or inimigo_y + TAMANHO_INIMIGO >= ALTURA:
    vel_y = -vel_y   # Inverte direção vertical
```

Por fim, desenhamos o inimigo:

```python
pygame.draw.rect(tela, VERMELHO, (inimigo_x, inimigo_y, TAMANHO_INIMIGO, TAMANHO_INIMIGO))
```

### Código da Parte 3

Acrescente as variáveis ao bloco de estado inicial (antes do laço principal):

```python
TAMANHO_INIMIGO = 40
VERMELHO        = (200, 40, 40)

inimigo_x = random.randint(0, LARGURA - TAMANHO_INIMIGO)
inimigo_y = random.randint(ALTURA_PLACAR, ALTURA - TAMANHO_INIMIGO)
vel_x     = random.choice([-4, -3, -2, 2, 3, 4])
vel_y     = random.choice([-4, -3, -2, 2, 3, 4])
```

E dentro do laço principal, **antes** de chamar `desenhar_mira()`:

```python
# ── Movimenta o inimigo ──────────────────────────────────────────────────────
inimigo_x += vel_x
inimigo_y += vel_y

# Rebatimento nas bordas
if inimigo_x <= 0 or inimigo_x + TAMANHO_INIMIGO >= LARGURA:
    vel_x = -vel_x
if inimigo_y <= ALTURA_PLACAR or inimigo_y + TAMANHO_INIMIGO >= ALTURA:
    vel_y = -vel_y

# Desenha o inimigo
pygame.draw.rect(tela, VERMELHO, (inimigo_x, inimigo_y, TAMANHO_INIMIGO, TAMANHO_INIMIGO))
```

### Conceitos da Parte 3

| Conceito | Descrição |
|----------|-----------|
| **`random.randint(a, b)`** | Gera um inteiro aleatório entre `a` e `b` (inclusive). Útil para posicionar elementos aleatoriamente. |
| **`random.choice(seq)`** | Escolhe um elemento aleatório de uma sequência. Usado aqui para definir a velocidade inicial. |
| **Vetor de velocidade** | Par `(vel_x, vel_y)` que define quanto o inimigo avança em cada eixo por frame. |
| **Rebatimento (bounce)** | Inverter o sinal de `vel_x` ou `vel_y` quando o objeto atinge a borda simula o reflexo físico. |
| **`pygame.draw.rect()`** | Desenha um retângulo na tela. Parâmetros: `(surface, cor, (x, y, largura, altura))`. |
| **Área de jogo** | A região abaixo do placar (`y >= ALTURA_PLACAR`) define onde o inimigo pode circular sem cobrir o HUD. |

---

## Parte 4 – Colisão e explosão

Agora vamos fechar o ciclo do jogo: verificar se o **tiro acerta o inimigo** e, quando isso acontece, exibir uma **explosão**, reposicionar o inimigo e incrementar a pontuação.

### Verificando se o tiro acerta o inimigo

O Pygame fornece a classe `pygame.Rect` para representar retângulos e verificar colisões. O método `collidepoint(x, y)` retorna `True` se o ponto `(x, y)` está dentro do retângulo:

```python
inimigo_rect = pygame.Rect(inimigo_x, inimigo_y, TAMANHO_INIMIGO, TAMANHO_INIMIGO)

if tiro and inimigo_rect.collidepoint(tiro[0], tiro[1]):
    # ACERTOU!
    pontos   += 10
    inimigo_x = random.randint(0, LARGURA - TAMANHO_INIMIGO)
    inimigo_y = random.randint(ALTURA_PLACAR, ALTURA - TAMANHO_INIMIGO)
    tiro      = None
```

> 💡 **`pygame.Rect(x, y, largura, altura)`** cria um objeto retângulo. Além de armazenar posição e dimensões, ele oferece métodos prontos de colisão como `collidepoint()`, `colliderect()`, e propriedades úteis como `centerx`, `centery`, `topleft`, etc.

> 💡 **`rect.collidepoint(x, y)`** retorna `True` se o ponto `(x, y)` está dentro do retângulo. É a forma mais simples de verificar se um tiro (um ponto) atingiu um objeto.

### Animando a explosão

Para a explosão, usamos uma variável de estado semelhante à do tiro:

```python
explosao = None  # None = sem explosão
                 # [cx, cy, frames_restantes] = explosão ativa
```

Quando um acerto é detectado, inicializamos a explosão no centro do inimigo:

```python
explosao = [inimigo_x + TAMANHO_INIMIGO // 2,
            inimigo_y + TAMANHO_INIMIGO // 2,
            30]   # Dura 30 frames
```

A animação cresce o raio do círculo conforme os frames diminuem e vai escurecendo a cor gradualmente:

```python
if explosao:
    progresso   = 30 - explosao[2]        # 0 → 30
    raio        = 5 + progresso * 2       # Cresce de 5 até 65 pixels
    intensidade = max(0, 255 - progresso * 8)
    cor_exp     = (255, intensidade // 2, 0)   # Laranja que escurece
    pygame.draw.circle(tela, cor_exp, (explosao[0], explosao[1]), raio)
    explosao[2] -= 1
    if explosao[2] <= 0:
        explosao = None
```

### Código da Parte 4

Acrescente **antes** do laço principal:

```python
explosao = None
LARANJA  = (255, 140, 0)
```

E dentro do laço, **após** desenhar o inimigo e **antes** de desenhar a mira:

```python
# ── Detecta colisão tiro ↔ inimigo ───────────────────────────────────────────
inimigo_rect = pygame.Rect(inimigo_x, inimigo_y, TAMANHO_INIMIGO, TAMANHO_INIMIGO)

if tiro and inimigo_rect.collidepoint(tiro[0], tiro[1]):
    explosao  = [inimigo_x + TAMANHO_INIMIGO // 2,
                 inimigo_y + TAMANHO_INIMIGO // 2, 30]
    pontos   += 10
    inimigo_x = random.randint(0, LARGURA - TAMANHO_INIMIGO)
    inimigo_y = random.randint(ALTURA_PLACAR, ALTURA - TAMANHO_INIMIGO)
    tiro      = None

# ── Anima a explosão ─────────────────────────────────────────────────────────
if explosao:
    progresso   = 30 - explosao[2]
    raio        = 5 + progresso * 2
    intensidade = max(0, 255 - progresso * 8)
    cor_exp     = (255, intensidade // 2, 0)
    pygame.draw.circle(tela, cor_exp, (explosao[0], explosao[1]), raio)
    explosao[2] -= 1
    if explosao[2] <= 0:
        explosao = None
```

### Conceitos da Parte 4

| Conceito | Descrição |
|----------|-----------|
| **`pygame.Rect`** | Classe que representa um retângulo com posição e dimensões. Oferece métodos de colisão e propriedades geométricas prontas. |
| **`rect.collidepoint(x, y)`** | Verifica se um ponto está dentro do retângulo. Retorna `True` ou `False`. |
| **Detecção ponto-retângulo** | Estratégia de colisão simples para tiros (pontos) contra inimigos (retângulos). |
| **Animação por frames** | Usar um contador de frames para controlar a duração e o progresso de uma animação (explosão crescendo). |
| **Interpolação de cor** | Calcular a cor da explosão frame a frame cria a ilusão de que ela "esfria" gradualmente. |
| **Reposicionamento** | Após o acerto, o inimigo reaparece em posição aleatória — técnica padrão de *respawn*. |

---

## Código completo comentado

```python
import pygame
import random

# ── 1. Inicialização ─────────────────────────────────────────────────────────
pygame.init()

LARGURA         = 800
ALTURA          = 600
ALTURA_PLACAR   = 50
TAMANHO_INIMIGO = 40

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Tiro – Pygame")

# ── 2. Cores ─────────────────────────────────────────────────────────────────
PRETO        = (0,   0,   0)
BRANCO       = (255, 255, 255)
CINZA_ESCURO = (30,  30,  30)
AMARELO      = (255, 220,   0)
AZUL_ESCURO  = (20,  40,  80)
AZUL_CLARO   = (40,  90, 160)
VERMELHO     = (200,  40,  40)
LARANJA      = (255, 140,   0)

# ── 3. Fontes ─────────────────────────────────────────────────────────────────
fonte_titulo = pygame.font.SysFont("Arial", 36, bold=True)
fonte_texto  = pygame.font.SysFont("Arial", 28)
fonte_placar = pygame.font.SysFont("Arial", 24, bold=True)

# ── 4. Funções auxiliares ─────────────────────────────────────────────────────
def desenhar_placar(tela, nome, pontos):
    """Desenha a faixa de placar no topo da janela."""
    pygame.draw.rect(tela, AZUL_ESCURO, (0, 0, LARGURA, ALTURA_PLACAR))
    texto = f"Jogador: {nome}          Pontos: {pontos}"
    surf  = fonte_placar.render(texto, True, BRANCO)
    tela.blit(surf, (20, 13))

def desenhar_mira(tela, pos):
    """Desenha uma mira (crosshair) na posição do mouse."""
    x, y = pos
    COR_MIRA  = (220, 50, 50)
    RAIO      = 12
    TAMANHO   = 18
    ESPESSURA = 2
    pygame.draw.line(tela, COR_MIRA, (x - TAMANHO, y), (x + TAMANHO, y), ESPESSURA)
    pygame.draw.line(tela, COR_MIRA, (x, y - TAMANHO), (x, y + TAMANHO), ESPESSURA)
    pygame.draw.circle(tela, COR_MIRA, (x, y), RAIO, ESPESSURA)

# ── 5. Tela de entrada do nome ────────────────────────────────────────────────
nome = ""
coletando_nome = True

while coletando_nome:
    tela.fill(CINZA_ESCURO)
    surf_inst = fonte_titulo.render("Digite seu nome e pressione Enter:", True, BRANCO)
    tela.blit(surf_inst, (LARGURA // 2 - surf_inst.get_width() // 2, 220))
    surf_nome = fonte_texto.render(nome + "|", True, AMARELO)
    tela.blit(surf_nome, (LARGURA // 2 - surf_nome.get_width() // 2, 290))
    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN and nome.strip():
                coletando_nome = False
            elif evento.key == pygame.K_BACKSPACE:
                nome = nome[:-1]
            else:
                nome += evento.unicode

# ── 6. Estado inicial do jogo ─────────────────────────────────────────────────
pontos   = 0
tiro     = None   # [x, y, frames_restantes] ou None
explosao = None   # [cx, cy, frames_restantes] ou None

inimigo_x = random.randint(0, LARGURA - TAMANHO_INIMIGO)
inimigo_y = random.randint(ALTURA_PLACAR, ALTURA - TAMANHO_INIMIGO)
vel_x     = random.choice([-4, -3, -2, 2, 3, 4])
vel_y     = random.choice([-4, -3, -2, 2, 3, 4])

relogio = pygame.time.Clock()
pygame.mouse.set_visible(False)   # Esconde o cursor do sistema

# ── 7. Laço principal ─────────────────────────────────────────────────────────
rodando = True

while rodando:
    # Fundo
    tela.fill(AZUL_CLARO)

    # Placar
    desenhar_placar(tela, nome, pontos)

    # Movimenta o inimigo
    inimigo_x += vel_x
    inimigo_y += vel_y

    # Rebate nas bordas
    if inimigo_x <= 0 or inimigo_x + TAMANHO_INIMIGO >= LARGURA:
        vel_x = -vel_x
    if inimigo_y <= ALTURA_PLACAR or inimigo_y + TAMANHO_INIMIGO >= ALTURA:
        vel_y = -vel_y

    # Desenha o inimigo
    pygame.draw.rect(tela, VERMELHO, (inimigo_x, inimigo_y, TAMANHO_INIMIGO, TAMANHO_INIMIGO))

    # Detecta colisão tiro ↔ inimigo
    inimigo_rect = pygame.Rect(inimigo_x, inimigo_y, TAMANHO_INIMIGO, TAMANHO_INIMIGO)
    if tiro and inimigo_rect.collidepoint(tiro[0], tiro[1]):
        explosao  = [inimigo_x + TAMANHO_INIMIGO // 2,
                     inimigo_y + TAMANHO_INIMIGO // 2, 30]
        pontos   += 10
        inimigo_x = random.randint(0, LARGURA - TAMANHO_INIMIGO)
        inimigo_y = random.randint(ALTURA_PLACAR, ALTURA - TAMANHO_INIMIGO)
        tiro      = None

    # Anima a explosão
    if explosao:
        progresso   = 30 - explosao[2]
        raio        = 5 + progresso * 2
        intensidade = max(0, 255 - progresso * 8)
        cor_exp     = (255, intensidade // 2, 0)
        pygame.draw.circle(tela, cor_exp, (explosao[0], explosao[1]), raio)
        explosao[2] -= 1
        if explosao[2] <= 0:
            explosao = None

    # Posição atual do mouse
    pos_mouse = pygame.mouse.get_pos()

    # Desenha o tiro (se ativo)
    if tiro:
        pygame.draw.circle(tela, AMARELO, (tiro[0], tiro[1]), 8)
        tiro[2] -= 1
        if tiro[2] <= 0:
            tiro = None

    # Desenha a mira por cima de tudo
    desenhar_mira(tela, pos_mouse)

    # Processa eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            tiro = [pos_mouse[0], pos_mouse[1], 15]

    pygame.display.flip()
    relogio.tick(60)

# ── 8. Encerramento ───────────────────────────────────────────────────────────
pygame.quit()
print(f"Fim de jogo! {nome} fez {pontos} ponto(s).")
```

### O que acontece ao executar

1. Uma tela de entrada pede o nome do jogador — o texto aparece em tempo real.
2. Ao pressionar **Enter**, o jogo começa: a janela exibe o **placar no topo** e um inimigo vermelho em movimento.
3. O cursor do sistema desaparece e é substituído pela **mira vermelha**.
4. Ao **clicar**, um flash amarelo aparece brevemente na posição clicada.
5. Se o flash coincidir com o inimigo, uma **explosão laranja** se expande no local, a pontuação sobe 10 pontos e o inimigo reaparece em outro ponto aleatório.
6. Fechar a janela encerra o programa e imprime o resultado no terminal.

---

## Conceitos trabalhados

| Conceito | Descrição |
|----------|-----------|
| **`pygame.mouse.set_visible(False)`** | Esconde o cursor padrão do SO para que possamos desenhá-lo manualmente. |
| **`pygame.mouse.get_pos()`** | Retorna a posição atual do mouse como tupla `(x, y)`. |
| **`pygame.draw.line()`** | Desenha uma linha reta entre dois pontos com cor e espessura definidas. |
| **`pygame.draw.circle()`** | Desenha um círculo preenchido (`espessura=0`) ou apenas contorno (`espessura>0`). |
| **`pygame.draw.rect()`** | Desenha um retângulo na tela; usado aqui para o inimigo e o fundo do placar. |
| **`random.randint(a, b)`** | Inteiro aleatório entre `a` e `b` — usado para posicionar o inimigo. |
| **`random.choice(seq)`** | Elemento aleatório de uma sequência — usado para a velocidade inicial do inimigo. |
| **Vetor de velocidade** | Par `(vel_x, vel_y)` que controla o deslocamento do inimigo por frame. |
| **Rebatimento** | Inverter o sinal de um componente da velocidade ao atingir a borda cria o efeito de reflexo. |
| **`pygame.Rect`** | Classe que representa um retângulo com métodos de colisão embutidos. |
| **`rect.collidepoint(x, y)`** | Verifica se um ponto está dentro do retângulo — usado para detectar acertos. |
| **Variável de estado** | Usar `None` ou lista com contador de frames para gerenciar eventos temporários (tiro, explosão). |
| **Animação por frames** | Controlar a aparência de uma animação incrementando/decrementando variáveis a cada frame. |
| **`relogio.tick(FPS)`** | Controla a taxa de atualização do jogo, garantindo velocidade consistente. |

---

## Desafios

### 🟢 Nível 1 — Fácil

1. **Mude as cores da mira:** experimente cores diferentes para a mira, como verde ou azul.
2. **Aumente a velocidade do inimigo:** modifique os valores de `vel_x` e `vel_y` e observe como isso afeta a dificuldade.
3. **Inimigo maior:** altere `TAMANHO_INIMIGO` para `60` ou `80` e veja como fica mais fácil acertar.

### 🟡 Nível 2 — Intermediário

4. **Múltiplos tiros:** permita que até 3 tiros estejam na tela ao mesmo tempo, armazenando-os em uma lista.
5. **Inimigo muda de cor:** altere a cor do inimigo a cada vez que ele rebate em uma borda. (Dica: use `random.randint(0, 255)` para gerar uma cor aleatória.)
6. **Velocidade crescente:** após cada acerto, aumente a velocidade do inimigo em 0.5 (tornando o jogo progressivamente mais difícil).

### 🔴 Nível 3 — Avançado

7. **Múltiplos inimigos:** crie uma lista com 3 inimigos e verifique colisão para cada um deles.
8. **Vidas do jogador:** adicione 3 vidas ao jogador. Cada vez que o inimigo tocar na borda inferior da tela, o jogador perde uma vida. Exiba as vidas no placar.
9. **Tela de Game Over:** quando as vidas chegarem a zero, exiba uma tela de fim de jogo com a pontuação final e uma opção de reiniciar pressionando Enter.

---

> 📚 **Recursos úteis:**
> - Documentação oficial do Pygame: <https://www.pygame.org/docs/>
> - Módulo de desenho: <https://www.pygame.org/docs/ref/draw.html>
> - Mouse: <https://www.pygame.org/docs/ref/mouse.html>
> - Rect e colisões: <https://www.pygame.org/docs/ref/rect.html>
> - Módulo `random` do Python: <https://docs.python.org/3/library/random.html>
