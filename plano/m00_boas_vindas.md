# Missão 0: Boas-vindas e o primeiro gráfico

> **Pergunta da missão:** como é o clima de Santa Helena ao longo do ano?
> **Quando:** no encontro 0, junto com o orientador, e depois em casa
> **Notebook:** `m00_climograma.ipynb`
> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com)
> 📓 **Notebook de exemplo:** [Exemplo 01: Climograma (abrir no Colab)](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/01_climograma.ipynb). O exemplo é feito para Santa Helena (e Curitiba); na seção ✍️ **Sua vez**, você repete para as capitais.

---

## O que é esta pesquisa (leia com calma)

Você já deve ter ouvido que "o clima está mudando". Mas como mostrar isso com números?

Os climatologistas agrupam os lugares em **classes de clima**. A mais famosa é a de **Köppen**: no mapa
clássico de Alvares et al. (2013), o oeste do Paraná aparece como **Cfa** (temperado, sem estação seca,
verão quente). Cada letra depende de uma regra simples. Por exemplo: se o mês mais frio tem média acima de
18 °C, o clima é tropical (letra **A**); se tem média abaixo, é temperado (letra **C**).

Agora imagine um lugar cujo mês mais frio tenha média de 17,5 °C. O clima é **C**, mas está a só **0,5 °C**
de virar **A**. Se ele esquentar um pouco, a classe muda.

**É isso que vamos medir: o quão perto cada lugar está de mudar de classe, e se essa distância está
diminuindo.** Chamamos essa distância de **folga**.

Vamos usar duas classificações:
- **Köppen**, que usa temperatura e chuva;
- **Thornthwaite**, que usa o **balanço hídrico**: quanto de água sobra ou falta no solo.

## Como este plano funciona

- A pesquisa está dividida em **missões**. Cada missão dura cerca de **3 semanas** e termina num encontro com
  o orientador.
- Em cada missão você vai aprender **uma ou duas coisas novas de programação**, sempre usadas para responder
  uma pergunta da pesquisa.
- Toda missão termina com um **entregável pequeno**: uma figura ou uma tabela, mais algumas frases
  explicando o que ela mostra.
- Você **não precisa saber programar**. Vamos aprender juntos, devagar.

## Três regras que facilitam a sua vida

1. **Regra dos 30 minutos.** Travou no mesmo erro por mais de 30 minutos? Pare, tire um print do erro e
   mande para o orientador, com o que você já tentou. Isso **não é falha**, faz parte do trabalho.
2. **Check-in na semana 2.** No meio de cada missão, mande uma mensagem curta: uma figura ou tabela (mesmo
   incompleta) e uma dúvida.
3. **Diário de bordo.** No fim de cada notebook, escreva três coisas:
   - **O que aprendi** (2 ou 3 frases);
   - **Erros que encontrei e como resolvi**;
   - **Dúvidas** (para levar ao encontro).

## Passo a passo

### 1. Organizar o Google Drive

📁 **[Clique aqui para abrir a pasta do projeto no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing)**

⚠️ **Passo obrigatório: adicionar um atalho no "Meu Drive"**

A pasta foi compartilhada com você, então ela aparece em **"Compartilhados comigo"**, e não em **"Meu
Drive"**. O Colab só encontra as pastas que estão no "Meu Drive". Por isso:

1. 📁 abra a pasta pelo link acima;
2. 🖱️ clique com o botão direito no nome da pasta (`mudanca_climatica_br`), no alto da tela;
3. ➕ escolha **Organizar → Adicionar atalho** (em algumas versões: **Adicionar atalho ao Drive**);
4. 🏠 escolha **Meu Drive** e confirme;
5. ✅ confira: em "Meu Drive" deve aparecer `mudanca_climatica_br`, com uma setinha no ícone.

> 💡 Sem esse atalho, todos os códigos com `/content/drive/MyDrive/mudanca_climatica_br` dão erro
> `FileNotFoundError`.

Dentro da pasta ficam:

```
mudanca_climatica_br/
├── dados/        → arquivos de dados (o orientador coloca no começo)
├── notebooks/    → os seus notebooks, um por missão
├── figuras/      → as figuras que você gerar
├── resultados/   → as tabelas que você gerar (CSV)
└── leituras/     → os artigos em PDF
```

### 2. Abrir o Google Colab

1. 🚀 **[Clique aqui para abrir o Google Colab](https://colab.research.google.com)** e entre com a sua conta
   Google.
2. Clique em **Novo notebook**.
3. Clique no nome no alto ("Untitled0.ipynb") e troque para `m00_climograma`.
4. Vá em **Arquivo → Mover** e escolha a pasta `mudanca_climatica_br/notebooks/`.

> 💡 Um **notebook** é um caderno com dois tipos de bloco (as **células**):
> - **célula de código:** onde você escreve comandos em Python e aperta ▶ para rodar;
> - **célula de texto:** onde você escreve explicações, como num caderno.

### 3. O primeiro código

Esta é a **única vez** em que você vai copiar e colar um código sem precisar entendê-lo inteiro. A ideia é
você ver, logo no primeiro dia, que com poucas linhas dá para fazer um gráfico de verdade.

Cole numa célula de código e aperte ▶:

```python
# -------------------------------------------------------------
# Climograma: chuva (barras) e temperatura (linha) de cada mês
# -------------------------------------------------------------

# Carrega a biblioteca que faz gráficos e dá a ela o apelido "plt"
import matplotlib.pyplot as plt

# Nomes dos meses, na ordem (é uma "lista": vários valores entre colchetes)
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Normal climatológica 1991-2020 de Santa Helena-PR (base do Xavier).
# É a média de 30 anos de cada mês.

# Temperatura média de cada mês, em °C (janeiro a dezembro)
temperatura = [27.0, 27.0, 26.3, 23.9, 20.3, 19.3,
               18.9, 20.8, 22.6, 24.6, 25.4, 26.5]

# Chuva de cada mês, em mm (janeiro a dezembro)
chuva = [172.4, 157.2, 131.5, 140.0, 183.1, 140.4,
         100.4, 84.1, 139.4, 227.8, 186.9, 186.6]

# Cria a figura (fig) e o primeiro eixo (eixo_chuva), com 8 x 4 polegadas
fig, eixo_chuva = plt.subplots(figsize=(8, 4))

# Desenha as barras de chuva no primeiro eixo
eixo_chuva.bar(meses, chuva, color='steelblue')
eixo_chuva.set_ylabel('Chuva (mm)')

# Cria um segundo eixo vertical, à direita, para a temperatura
eixo_temperatura = eixo_chuva.twinx()

# Desenha a linha de temperatura, com uma bolinha em cada mês
eixo_temperatura.plot(meses, temperatura, color='red', marker='o')
eixo_temperatura.set_ylabel('Temperatura (°C)')

# Título do gráfico
eixo_chuva.set_title('Climograma de Santa Helena-PR')

# Mostra o gráfico na tela
plt.show()
```

> 🧠 **Repare:** toda linha que começa com `#` é um **comentário**. O Python ignora essas linhas; elas
> servem para **explicar** o código para quem lê. Você vai escrever muitos comentários ao longo do projeto.

### 4. Brincar um pouco (em casa)

Mude **uma coisa por vez**, rode de novo e veja o que acontece:

1. Troque `'steelblue'` por `'green'`.
2. Troque o título para o nome da sua cidade.
3. Troque `marker='o'` por `marker='s'`.
4. Troque a chuva de julho (`100.4`) por `300` e veja o gráfico. Depois volte ao valor original.

Se aparecer um erro, **não se assuste**: leia a última linha da mensagem vermelha e anote no diário.

### 5. Salvar a figura

Acrescente esta linha **antes** de `plt.show()`:

```python
# Salva a figura na pasta "figuras" do Drive (o Colab vai pedir permissão para acessar o Drive)
fig.savefig('/content/drive/MyDrive/mudanca_climatica_br/figuras/climograma_santa_helena.png', dpi=200)
```

Para o Colab enxergar o Drive, rode antes, numa célula separada:

```python
# Conecta o Colab ao seu Google Drive
from google.colab import drive
drive.mount('/content/drive')
```

---

## 📖 Leitura

Alvares et al. (2013), só a **introdução** (está em `leituras/`). Não precisa entender tudo; sublinhe as
palavras que não conhecer.

## 📦 Entregável

- ✍️ A seção **Sua vez** do notebook de exemplo, feita para as capitais pedidas.
- A figura `climograma_santa_helena.png` (com os valores originais).
- Uma célula de texto no notebook respondendo:
  1. Qual o mês mais quente? E o mais frio?
  2. Qual o mês mais chuvoso? E o mais seco?
  3. Existe uma "estação seca" bem marcada em Santa Helena?
- O diário de bordo preenchido.

## 🗣️ Para o próximo encontro, saiba responder

- O que é uma célula de código? E uma de texto?
- Para que serve o `#`?
- O que a linha `eixo_chuva.bar(meses, chuva, color='steelblue')` faz?

## ✅ Checklist

- [ ] Abri o Colab e criei o notebook na pasta certa
- [ ] Rodei o climograma
- [ ] Fiz as 4 mudanças do passo 4
- [ ] Salvei a figura
- [ ] Li a introdução de Alvares et al. (2013)
- [ ] Preenchi o diário de bordo
