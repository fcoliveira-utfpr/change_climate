# Missão 6: A série histórica, 65 anos de clima

> **Pergunta da missão:** a temperatura e a chuva de Santa Helena mudaram de 1961 a 2025?
> **Duração:** 3 semanas
> **Notebook:** `m05_serie_historica.ipynb`
> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com)
> 📓 **Notebook de exemplo:** [Exemplo 07: Série histórica (abrir no Colab)](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/07_serie_historica.ipynb). O exemplo é feito para Santa Helena (e Curitiba); na seção ✍️ **Sua vez**, você repete para as capitais.
> **Início da fase 2:** o clima muda no tempo

---

## Por que isso importa

Até aqui você usou **uma** normal (12 números de temperatura e 12 de chuva). Agora vai trabalhar com a
**série completa**: um valor por mês, de janeiro de 1961 a dezembro de 2025. São 780 meses.

Os dados vêm da **base do Xavier** (BR-DWGD), uma grade de dados meteorológicos diários do Brasil inteiro,
construída a partir de milhares de estações. A base fica no **Google Earth Engine**, uma plataforma do Google
na nuvem. Na **Missão 5** você extraiu essa série no Earth Engine e conferiu que ela é igual ao arquivo
`santa_helena_mensal.csv` do projeto. Também extraiu as 27 capitais, que vai usar na seção ✍️ **Sua vez** do
notebook de exemplo.

## O que você vai aprender de Python

- **ler um arquivo CSV** (uma planilha em texto);
- trabalhar com **datas**;
- calcular a **média anual** a partir dos meses.

> 💡 A partir desta missão você **pode copiar os modelos de código**, mas precisa **completar as lacunas**
> (`___`) e **entender cada comentário**.

---

## Semana 1: abrir e olhar os dados

### Conectar o Drive e ler o arquivo

```python
# Conecta o Colab ao Google Drive
from google.colab import drive
drive.mount('/content/drive')
```

```python
import pandas as pd
import matplotlib.pyplot as plt

# Endereço da pasta do projeto no Drive.
# Guardamos numa variável para não repetir o texto toda hora.
BASE = '/content/drive/MyDrive/mudanca_climatica_br'

# Endereço completo do arquivo.
# O f antes das aspas permite colocar uma variável dentro do texto, entre { }.
# Assim, {BASE} é trocado pelo endereço da pasta.
arquivo = f'{BASE}/dados/santa_helena_mensal.csv'

# Lê o arquivo CSV e cria uma tabela.
#   parse_dates=['data'] -> a coluna 'data' deve ser entendida como DATA, não como texto
#   index_col='data'     -> a coluna 'data' vira o "índice" (o nome de cada linha)
serie = pd.read_csv(arquivo, parse_dates=['data'], index_col='data')
```

### Olhar os dados (sempre faça isso primeiro!)

Rode cada linha numa célula separada e anote o que cada uma mostra:

```python
# As 5 primeiras linhas
serie.head()
```

```python
# As 5 últimas linhas
serie.tail()
```

```python
# Quantas linhas (meses) a tabela tem
len(serie)
```

```python
# Resumo: média, mínimo, máximo etc. de cada coluna
serie.describe()
```

> 🧠 **Confira:** 1961 a 2025 são 65 anos. 65 × 12 = ? O número de linhas bate?
> Os valores mínimo e máximo de temperatura e chuva fazem sentido para Santa Helena?

---

## Semana 2: da série mensal para a série anual

```python
# Temperatura média de cada ano: a média dos 12 meses.
#   resample('YS') agrupa os meses por ano ("Year Start")
#   .mean() tira a média de cada grupo
temperatura_anual = serie['tmed'].resample('YS').mean()

# Chuva total de cada ano: a SOMA dos 12 meses
chuva_anual = serie['chuva'].resample('YS').sum()

# Mostra os primeiros anos
temperatura_anual.head()
```

> 🧠 **Por que temperatura usa `.mean()` e chuva usa `.sum()`?** Escreva a resposta no diário.

### O gráfico da série anual

```python
# Figura com 2 gráficos, um em cima do outro, com o mesmo eixo de anos
fig, eixos = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# .index.year pega só o ANO de cada data (1961, 1962, ...)
anos = temperatura_anual.index.year

# Gráfico de cima: temperatura
eixos[0].plot(anos, temperatura_anual, marker='o', color='red')
eixos[0].set_ylabel('Temperatura média (°C)')
eixos[0].grid(alpha=0.3)            # grade clarinha ao fundo

# Gráfico de baixo: chuva
eixos[1].bar(anos, chuva_anual, color='steelblue')
eixos[1].set_ylabel('Chuva anual (mm)')
eixos[1].set_xlabel('Ano')
eixos[1].grid(alpha=0.3)

fig.suptitle('Santa Helena-PR, 1961-2025 (Xavier)')
plt.tight_layout()

# Salva e mostra
fig.savefig(f'{BASE}/figuras/serie_anual_santa_helena.png', dpi=200)
plt.show()
```

---

## Semana 3: primeiras perguntas à série

```python
# O ano mais quente e o mais frio
print('Ano mais quente:', temperatura_anual.idxmax().year, '-', round(temperatura_anual.max(), 2), '°C')
print('Ano mais frio:', temperatura_anual.idxmin().year, '-', round(temperatura_anual.min(), 2), '°C')

# O ano mais chuvoso e o mais seco
print('Ano mais chuvoso:', chuva_anual.idxmax().year, '-', round(chuva_anual.max()), 'mm')
print('Ano mais seco:', chuva_anual.idxmin().year, '-', round(chuva_anual.min()), 'mm')
```

```python
# Média de temperatura de duas décadas, para comparar.
# .loc['1961':'1970'] recorta só os anos de 1961 a 1970.
media_decada_1960 = temperatura_anual.loc['1961':'1970'].mean()
media_decada_2010 = temperatura_anual.loc['___':'___'].mean()   # complete: 2016 a 2025

print('Média 1961-1970:', round(media_decada_1960, 2), '°C')
print('Média 2016-2025:', round(media_decada_2010, 2), '°C')
print('Diferença:', round(media_decada_2010 - media_decada_1960, 2), '°C')
```

> ⚠️ **Um ano quente não é mudança climática.** Um ano é **variabilidade**; mudança climática é a média de
> muitos anos se deslocando. É por isso que, na Missão 7, vamos comparar períodos de **30 anos**.

### 📖 Leitura

Xavier et al. (2022), introdução e seção de dados. Responda no diário: **como a grade foi construída?** Por
que, em regiões com poucas estações, os dados são menos confiáveis?

---

## Se der erro

| Mensagem | O que costuma ser |
|---|---|
| `FileNotFoundError` | o endereço do arquivo está errado; confira o nome da pasta e do arquivo no Drive |
| `KeyError: 'tmed'` | o nome da coluna está diferente; rode `serie.columns` para ver os nomes |

## 📦 Entregável

- ✍️ A seção **Sua vez** do notebook de exemplo, feita para as capitais pedidas.
- A figura `serie_anual_santa_helena.png`.
- Uma célula de texto com:
  1. o ano mais quente, o mais frio, o mais chuvoso e o mais seco;
  2. a diferença de temperatura entre 1961–1970 e 2016–2025;
  3. olhando o gráfico: a temperatura parece estar subindo? E a chuva?

## 🗣️ Para o próximo encontro, saiba responder

- O que faz `resample('YS')`?
- Por que a temperatura anual usa média e a chuva anual usa soma?
- Qual a diferença entre variabilidade e mudança climática?

## ✅ Checklist

- [ ] Li o arquivo e conferi o número de linhas
- [ ] Calculei a série anual de temperatura e chuva
- [ ] Fiz e salvei o gráfico
- [ ] Respondi às perguntas da semana 3
- [ ] Li Xavier et al. (2022)
- [ ] Preenchi o diário de bordo
