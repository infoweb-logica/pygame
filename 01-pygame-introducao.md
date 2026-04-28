# Introdução ao Pygame

## Sumário

1. [O que é o Pygame?](#o-que-é-o-pygame)
2. [Instalação](#instalação)
3. [Estrutura básica de um programa Pygame](#estrutura-básica-de-um-programa-pygame)
4. [Criando a janela](#criando-a-janela)
5. [Modificando o título da janela](#modificando-o-título-da-janela)
6. [O laço principal de eventos](#o-laço-principal-de-eventos)
7. [Aguardando um clique para encerrar](#aguardando-um-clique-para-encerrar)
8. [Código completo comentado](#código-completo-comentado)
9. [Conceitos trabalhados](#conceitos-trabalhados)
10. [Desafios](#desafios)

---

## O que é o Pygame?

**Pygame** é uma biblioteca de código aberto para Python que facilita o desenvolvimento de jogos e aplicações multimídia. Ela fornece módulos para:

- Criar e gerenciar **janelas gráficas**
- Desenhar formas, imagens e texto na tela
- Reproduzir **sons e músicas**
- Capturar entradas do teclado e do **mouse**
- Controlar o tempo (FPS — *frames per second*)

O Pygame é amplamente usado em cursos de programação porque permite visualizar conceitos de programação de forma interativa, tornando o aprendizado mais dinâmico e divertido.

> 💡 **Curiosidade:** O Pygame é construído sobre a biblioteca SDL (*Simple DirectMedia Layer*), escrita em C, o que garante boa performance mesmo sendo usada a partir do Python.

---

## Instalação

Antes de começar, certifique-se de ter o Python instalado (versão 3.7 ou superior). Para instalar o Pygame, abra o terminal e execute:

```bash
pip install pygame
```

Para verificar se a instalação foi bem-sucedida, execute no terminal:

```bash
python -m pygame --version
```

Você deverá ver a versão do Pygame impressa na tela.

---

## Estrutura básica de um programa Pygame

Todo programa Pygame segue uma estrutura em três etapas:

```
1. Inicialização  →  pygame.init()
2. Laço principal →  while True: (captura eventos, atualiza estado, desenha)
3. Encerramento   →  pygame.quit()
```

Essa estrutura reflete como jogos e aplicações interativas funcionam na prática: eles ficam em um **laço contínuo** processando eventos (teclas pressionadas, cliques de mouse, etc.) e redesenhando a tela até que o usuário decida encerrar.

---

## Criando a janela

Para criar uma janela no Pygame, utilizamos a função `pygame.display.set_mode()`, que recebe uma **tupla** com a largura e a altura da janela em pixels:

```python
import pygame

pygame.init()

# Cria uma janela de 800x600 pixels
tela = pygame.display.set_mode((800, 600))
```

- O parâmetro `(800, 600)` é uma **tupla** — note os dois pares de parênteses: um para a função e outro para a tupla.
- A função retorna um objeto do tipo `Surface`, que representa a janela onde iremos desenhar.
- `pygame.init()` inicializa **todos** os módulos do Pygame de uma vez. É sempre a primeira chamada em um programa Pygame.

---

## Modificando o título da janela

Por padrão, o Pygame exibe `"pygame window"` na barra de título. Para personalizar esse título, usamos:

```python
pygame.display.set_caption("Meu Primeiro Programa")
```

Essa função deve ser chamada **após** `pygame.init()` e **antes** do laço principal para que o título apareça assim que a janela abrir.

---

## O laço principal de eventos

O **laço principal** (também chamado de *game loop*) é o coração de qualquer programa Pygame. Ele mantém a janela aberta e processa continuamente os eventos gerados pelo usuário e pelo sistema:

```python
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

pygame.quit()
```

A cada iteração do laço:
1. `pygame.event.get()` retorna a **lista de eventos** que ocorreram desde a última iteração.
2. Cada evento possui um `type` (tipo) que identifica o que aconteceu.
3. `pygame.QUIT` é o evento disparado quando o usuário clica no **X** da janela.

---

## Aguardando um clique para encerrar

Além de fechar pela barra de título, podemos encerrar o programa quando o usuário **clicar em qualquer lugar na tela**. O evento correspondente a um clique do mouse é `pygame.MOUSEBUTTONDOWN`:

```python
for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
        rodando = False
    if evento.type == pygame.MOUSEBUTTONDOWN:
        rodando = False
```

O evento `MOUSEBUTTONDOWN` é disparado no momento em que **qualquer botão** do mouse é pressionado. Se quiser verificar apenas o botão esquerdo, você pode usar:

```python
if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
    rodando = False
```

> **Referência rápida de botões:**
> - `evento.button == 1` → botão esquerdo
> - `evento.button == 2` → botão do meio (scroll)
> - `evento.button == 3` → botão direito

---

## Código completo comentado

```python
import pygame  # Importa a biblioteca Pygame

# ── 1. Inicialização ────────────────────────────────────────────────────────
pygame.init()  # Inicializa todos os módulos do Pygame

# ── 2. Configuração da janela ───────────────────────────────────────────────
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))  # Cria a janela
pygame.display.set_caption("Meu Primeiro Pygame")  # Define o título

# Define a cor de fundo (formato RGB: Vermelho, Verde, Azul — valores de 0 a 255)
COR_FUNDO = (30, 30, 30)  # Cinza escuro

# ── 3. Laço principal ───────────────────────────────────────────────────────
rodando = True

while rodando:
    # Preenche a tela com a cor de fundo a cada frame
    tela.fill(COR_FUNDO)

    # Processa todos os eventos pendentes
    for evento in pygame.event.get():

        # Clique no botão X da janela
        if evento.type == pygame.QUIT:
            rodando = False

        # Clique do mouse dentro da janela
        if evento.type == pygame.MOUSEBUTTONDOWN:
            print(f"Clique detectado em: {evento.pos}")  # Exibe a posição do clique
            rodando = False

    # Atualiza o conteúdo exibido na janela
    pygame.display.flip()

# ── 4. Encerramento ─────────────────────────────────────────────────────────
pygame.quit()
print("Programa encerrado.")
```

### O que acontece ao executar

1. Uma janela de 800 × 600 pixels abre com fundo cinza escuro e título **"Meu Primeiro Pygame"**.
2. A janela permanece aberta e responsiva aguardando um evento.
3. Ao **clicar em qualquer lugar** na janela (ou fechar pelo X), o laço é encerrado.
4. A posição do clique é impressa no terminal antes de encerrar.

---

## Conceitos trabalhados

| Conceito | Descrição |
|----------|-----------|
| **Importação de biblioteca** | `import pygame` disponibiliza todos os recursos da biblioteca no programa. |
| **Inicialização de sistema** | `pygame.init()` prepara os módulos internos antes do uso. |
| **Tupla** | Estrutura imutável usada para representar pares de valores, como dimensões `(800, 600)` e cores `(255, 0, 0)`. |
| **Surface** | Objeto que representa uma área de desenho; a janela principal é uma Surface. |
| **Laço principal (*game loop*)** | Estrutura `while` que mantém o programa em execução e processa eventos continuamente. |
| **Evento** | Ação do usuário ou do sistema (fechar janela, clicar, pressionar tecla) capturada por `pygame.event.get()`. |
| **Modelo de cores RGB** | Cores definidas por três componentes: Vermelho (*Red*), Verde (*Green*) e Azul (*Blue*), cada um variando de 0 a 255. |
| **`display.flip()`** | Atualiza a janela exibindo tudo que foi desenhado no frame atual. |

---

## Desafios

### 🟢 Nível 1 — Fácil

1. **Mude a cor de fundo:** altere `COR_FUNDO` para exibir a janela com fundo azul `(0, 0, 255)`, depois tente vermelho e verde.
2. **Mude o título:** personalize `set_caption` com o seu nome.
3. **Altere o tamanho da janela:** experimente dimensões diferentes, como `(400, 400)` ou `(1024, 768)`.

### 🟡 Nível 2 — Intermediário

4. **Exiba as coordenadas do clique:** modifique o programa para que, em vez de encerrar, cada clique **imprima a posição** `(x, y)` no terminal, e apenas o botão direito encerre o programa.
5. **Contagem de cliques:** adicione uma variável `contador` que incremente a cada clique e exiba o valor no terminal a cada vez. Encerre somente após **3 cliques**.
6. **Cor aleatória:** a cada clique, altere a cor de fundo para uma cor **aleatória** usando `random.randint(0, 255)`.

### 🔴 Nível 3 — Avançado

7. **Desenhe onde clicou:** use `pygame.draw.circle(tela, cor, posicao, raio)` para desenhar um círculo na posição de cada clique. O programa só deve encerrar quando o usuário fechar pelo X.
8. **Pressione uma tecla para encerrar:** além do clique, adicione suporte para que pressionar a tecla `ESC` também encerre o programa. (Dica: use o evento `pygame.KEYDOWN` e `evento.key == pygame.K_ESCAPE`.)
9. **Mini tela de boas-vindas:** exiba um texto "Clique para iniciar" no centro da janela usando `pygame.font.SysFont`. O programa só deve avançar após o clique.

---

> 📚 **Recursos úteis:**
> - Documentação oficial do Pygame: <https://www.pygame.org/docs/>
> - Lista completa de eventos: <https://www.pygame.org/docs/ref/event.html>
> - Lista de teclas (`K_*`): <https://www.pygame.org/docs/ref/key.html>
