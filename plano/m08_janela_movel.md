# Missão 8: A janela móvel, um clima para cada ano

> **Pergunta da missão:** **quando** as folgas começaram a diminuir? A classe chegou a oscilar?
> **Duração:** 3 semanas (é a missão mais importante da fase 2; se precisar, use 2 ciclos)
> **Notebook:** `m07_janela_movel.ipynb`
> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com)
> 📓 **Notebook de exemplo:** [Exemplo 09: Janela móvel (abrir no Colab)](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/09_janela_movel.ipynb). O exemplo é feito para Santa Helena (e Curitiba); na seção ✍️ **Sua vez**, você repete para as capitais.

---

## Por que isso importa

Com duas normais, temos **dois retratos** do clima. Com a **janela móvel**, temos **um retrato por ano**:

| Ano | Clima calculado com |
|---|---|
| 1990 | 1961–1990 |
| 1991 | 1962–1991 |
| 1992 | 1963–1992 |
| ... | ... |
| 2025 | 1996–2025 |

A cada ano, entra um ano novo e sai o mais antigo. São **36 climas** (de 1990 a 2025), e para cada um
calculamos a classe e as folgas. Assim dá para ver **quando** a folga começou a diminuir e se a classe
**oscilou** (por exemplo, Cfa → Cwa → Cfa), sinal de que o clima está "na beirada" da classe.

> Este método não é a normal oficial da OMM. Por isso o chamamos de **clima de referência móvel**.

## O que você vai aprender de Python

- **repetição com `for`:** fazer a mesma coisa para cada ano, sem escrever o código 36 vezes.

---

## Semana 1: aprender o `for` com calma

Rode cada exemplo e **preveja o resultado antes**:

```python
# Exemplo 1: o for repete as linhas recuadas (com 4 espaços) para cada valor da lista
for ano in [1990, 1991, 1992]:
    print('O clima de', ano, 'usa os anos de', ano - 29, 'até', ano)
```

```python
# Exemplo 2: range(1990, 1996) gera os números 1990, 1991, ..., 1995 (o último NÃO entra)
for ano in range(1990, 1996):
    print(ano)
```

```python
# Exemplo 3: guardar resultados numa lista que começa vazia
resultados = []                       # lista vazia
for ano in range(1990, 1996):
    inicio = ano - 29
    resultados.append(inicio)         # .append acrescenta um valor no fim da lista
print(resultados)
```

> 🧠 **Pergunta:** para gerar os anos de 1990 a **2025**, qual deve ser o segundo número do `range`?

### Um ano só, antes do for

Antes de repetir para todos os anos, faça **um ano só** (2000), juntando o que você aprendeu na Missão 7:

```python
from google.colab import drive
drive.mount('/content/drive')
!pip install agrometeorologiapy

import agrometeorologiapy as amp
import pandas as pd
import matplotlib.pyplot as plt

BASE = '/content/drive/MyDrive/mudanca_climatica_br'
LATITUDE = -24.86
serie = pd.read_csv(f'{BASE}/dados/santa_helena_mensal.csv', parse_dates=['data'], index_col='data')
```

```python
ano = 2000

# Primeiro e último ano da janela de 30 anos que termina em "ano"
primeiro_ano = ano - 29
ultimo_ano = ano

# Recorta a janela. str() transforma o número em texto, que é o que o .loc espera aqui.
janela = serie.loc[str(primeiro_ano):str(ultimo_ano)]

# Normal da janela: média de cada mês
normal = janela.groupby(janela.index.month).mean()
temperatura = normal['tmed'].tolist()
chuva = normal['chuva'].tolist()

# Köppen
koppen = amp.classificacao_koppen(temperatura, chuva, LATITUDE)
print(ano, koppen['classe'])
```

---

## Semana 2: o `for` com Köppen

Agora coloque o bloco acima **dentro** de um `for`. Repare que é o mesmo código, só que recuado:

```python
# Lista vazia que vai receber uma "linha" de resultados para cada ano
linhas = []

for ano in range(1990, 2026):

    # --- janela de 30 anos que termina em "ano" ---
    primeiro_ano = ano - 29
    ultimo_ano = ano
    janela = serie.loc[str(primeiro_ano):str(ultimo_ano)]

    # --- normal da janela ---
    normal = janela.groupby(janela.index.month).mean()
    temperatura = normal['tmed'].tolist()
    chuva = normal['chuva'].tolist()

    # --- Köppen ---
    koppen = amp.classificacao_koppen(temperatura, chuva, LATITUDE)

    # --- folgas de Köppen ---
    folga_A = min(temperatura) - 18
    folga_a = max(temperatura) - 22
    folga_f = min(chuva) - 60

    # --- guarda os resultados deste ano num dicionário ---
    linha = {
        'ano': ano,
        'periodo': str(primeiro_ano) + '-' + str(ultimo_ano),
        'koppen': koppen['classe'],
        'folga_A': folga_A,
        'folga_a': folga_a,
        'folga_f': folga_f,
    }
    linhas.append(linha)

# Fora do for (sem recuo): transforma a lista de linhas numa tabela
resultado = pd.DataFrame(linhas)

# Usa a coluna 'ano' como índice (o nome de cada linha)
resultado = resultado.set_index('ano')

resultado.round(2)
```

> 🧠 **Confira:** a linha de 1990 é igual à normal 1961–1990 da Missão 7? E a de 2020 é igual à de
> 1991–2020? Se for, o seu `for` está certo.

---

## Semana 3: Thornthwaite, gráficos e oscilações

### Acrescentar Thornthwaite

Dentro do `for`, **depois** do Köppen, acrescente:

```python
    # --- Thornthwaite ---
    tabela_etp = amp.thornthwaite_mensal(pd.DataFrame({'T_media_C': temperatura}), lat=LATITUDE)
    etp = tabela_etp['ETP_mm_mes']
    thornthwaite = amp.classificacao_thornthwaite(chuva, etp, LATITUDE)
```

E, no dicionário `linha`, acrescente três itens:

```python
        'thornthwaite': thornthwaite['classe'],
        'Im': thornthwaite['Im'],
        'ETP_anual': thornthwaite['ETP_anual'],
```

Rode tudo de novo e salve a tabela:

```python
resultado.round(3).to_csv(f'{BASE}/resultados/janela_movel_santa_helena.csv')
```

### Gráficos das folgas no tempo

```python
fig, eixos = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

# Folga A/C
eixos[0].plot(resultado.index, resultado['folga_A'], marker='o', color='tomato')
eixos[0].axhline(0, color='black', linestyle='--')     # o limiar
eixos[0].set_ylabel('Folga A/C (°C)')

# Folga a/b
eixos[1].plot(resultado.index, resultado['folga_a'], marker='o', color='orange')
eixos[1].axhline(0, color='black', linestyle='--')
eixos[1].set_ylabel('Folga a/b (°C)')

# Im de Thornthwaite
eixos[2].plot(resultado.index, resultado['Im'], marker='o', color='steelblue')
eixos[2].set_ylabel('Im (%)')
eixos[2].set_xlabel('Ano (fim da janela de 30 anos)')

for eixo in eixos:
    eixo.grid(alpha=0.3)

fig.suptitle('Clima de referência móvel: Santa Helena-PR')
plt.tight_layout()
fig.savefig(f'{BASE}/figuras/janela_movel_santa_helena.png', dpi=200)
plt.show()
```

> 💡 No gráfico do Im, desenhe também os limites de classe mais próximos com `axhline`, como fizemos com o
> zero. Quais limites você escolheria?

### A classe oscilou?

```python
# Quantas vezes cada classe aparece
print(resultado['koppen'].value_counts())
print(resultado['thornthwaite'].value_counts())
```

```python
# Em que anos a classe de Köppen mudou em relação ao ano anterior?
#   .shift() empurra a coluna uma linha para baixo: cada ano fica ao lado do ano anterior
classe_do_ano_anterior = resultado['koppen'].shift()

# True quando a classe é diferente da do ano anterior
mudou = resultado['koppen'] != classe_do_ano_anterior

# O primeiro ano não tem ano anterior, então não conta
mudou = mudou.iloc[1:]

# Pega os anos (o índice) em que "mudou" é True
anos_que_mudaram = mudou[mudou == True].index

# Mostra só esses anos, com o período e a classe
print('Anos em que a classe de Köppen mudou:')
print(resultado.loc[anos_que_mudaram, ['periodo', 'koppen']])
```

> 🧠 Se a classe muda e volta (Cfa → Cwa → Cfa), o clima está **na beirada** de um limiar. Mudança
> consistente é a que **permanece**.

> ⚠️ **Não aplique teste de tendência a estas curvas.** Janelas vizinhas compartilham 29 anos, então os
> valores "andam juntos" e qualquer teste daria significância falsa. O ritmo da mudança é medido na Missão
> 9, com a série **anual**.

---

## 📦 Entregável

- ✍️ A seção **Sua vez** do notebook de exemplo, feita para as capitais pedidas.
- O arquivo `resultados/janela_movel_santa_helena.csv`.
- A figura `janela_movel_santa_helena.png`.
- Um parágrafo respondendo: **as folgas diminuíram ao longo do tempo? A partir de quando? A classe oscilou?**

## 🗣️ Para o próximo encontro, saiba responder

- O que faz o `for`? E o `.append`?
- Por que o primeiro ano classificável é 1990?
- Por que não se aplica teste de tendência à curva da janela móvel?

## ✅ Checklist

- [ ] Rodei e entendi os 3 exemplos de `for`
- [ ] Fiz um ano só (2000) antes do `for`
- [ ] Rodei o `for` de 1990 a 2025 com Köppen
- [ ] Acrescentei Thornthwaite
- [ ] Conferi 1990 e 2020 com a Missão 7
- [ ] Fiz o gráfico e procurei oscilações
- [ ] Preenchi o diário de bordo
