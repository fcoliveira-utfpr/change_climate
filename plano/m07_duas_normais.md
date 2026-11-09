# Missão 7: Duas normais, o antes e o depois

> **Pergunta da missão:** o clima de 1991–2020 é diferente do de 1961–1990? As folgas diminuíram?
> **Duração:** 3 semanas
> **Notebook:** `m06_duas_normais.ipynb`
> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com)
> 📓 **Notebook de exemplo:** [Exemplo 08: Duas normais (abrir no Colab)](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/08_duas_normais.ipynb). O exemplo é feito para Santa Helena (e Curitiba); na seção ✍️ **Sua vez**, você repete para as capitais.

---

## Por que isso importa

A **normal climatológica** é a média de 30 anos. Os dois períodos, 1961–1990 e 1991–2020, **não se
sobrepõem**: são dois climas independentes. Compará-los é a forma mais simples e honesta de ver se o clima
mudou.

Nesta missão você vai **calcular** as normais a partir da série (e não mais digitá-las) e repetir, para os
dois períodos, tudo o que fez na fase 1: Köppen, Thornthwaite e as folgas.

## O que você vai aprender de Python

- **recortar um período** da série (`.loc['1961':'1990']`);
- **média por mês** (`groupby`): juntar todos os janeiros, todos os fevereiros etc.;
- transformar uma coluna em **lista** (`.tolist()`).

---

## Semana 1: calcular uma normal

```python
from google.colab import drive
drive.mount('/content/drive')

!pip install agrometeorologiapy
import agrometeorologiapy as amp
import pandas as pd
import matplotlib.pyplot as plt

BASE = '/content/drive/MyDrive/mudanca_climatica_br'
LATITUDE = -24.86

# Lê a série mensal (como na Missão 6)
serie = pd.read_csv(f'{BASE}/dados/santa_helena_mensal.csv', parse_dates=['data'], index_col='data')
```

```python
# 1) Recorta só os meses de 1961 a 1990
periodo_antes = serie.loc['1961':'1990']

# 2) Agrupa os meses pelo número do mês (1 = jan, 2 = fev, ..., 12 = dez)
#    e tira a média de cada grupo.
#    Resultado: 12 linhas, a média de todos os janeiros, de todos os fevereiros etc.
normal_antes = periodo_antes.groupby(periodo_antes.index.month).mean()

normal_antes
```

> 🧠 **Confira:** quantas linhas tem `periodo_antes`? (30 anos × 12 meses = ?) E `normal_antes`?

> 💡 A média da chuva de todos os janeiros é a **chuva normal de janeiro**. Somando os 12 meses da normal,
> obtém-se a chuva anual normal.

Agora faça o mesmo para 1991–2020:

```python
periodo_depois = serie.loc['___':'___']
normal_depois = periodo_depois.groupby(periodo_depois.index.month).mean()
```

### O climograma dos dois períodos

```python
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

fig, eixos = plt.subplots(1, 2, figsize=(11, 4))

# Temperatura: uma linha para cada período
eixos[0].plot(meses, normal_antes['tmed'], marker='o', color='gray', label='1961-1990')
eixos[0].plot(meses, normal_depois['tmed'], marker='o', color='red', label='1991-2020')
eixos[0].set_ylabel('Temperatura (°C)')
eixos[0].legend()

# Chuva: uma linha para cada período
eixos[1].plot(meses, normal_antes['chuva'], marker='o', color='gray', label='1961-1990')
eixos[1].plot(meses, normal_depois['chuva'], marker='o', color='steelblue', label='1991-2020')
eixos[1].set_ylabel('Chuva (mm)')
eixos[1].legend()

fig.suptitle('Normais climatológicas de Santa Helena-PR')
plt.tight_layout()
fig.savefig(f'{BASE}/figuras/duas_normais_santa_helena.png', dpi=200)
plt.show()
```

---

## Semana 2: classificar os dois períodos

As funções da biblioteca recebem **listas**. Por isso, transformamos as colunas em listas com `.tolist()`.

```python
# ---------- 1961-1990 ----------
temperatura_antes = normal_antes['tmed'].tolist()
chuva_antes = normal_antes['chuva'].tolist()

# Köppen
koppen_antes = amp.classificacao_koppen(temperatura_antes, chuva_antes, LATITUDE)

# Thornthwaite: primeiro a ETP, depois a classificação
tabela_etp_antes = amp.thornthwaite_mensal(pd.DataFrame({'T_media_C': temperatura_antes}), lat=LATITUDE)
etp_antes = tabela_etp_antes['ETP_mm_mes']
thornthwaite_antes = amp.classificacao_thornthwaite(chuva_antes, etp_antes, LATITUDE)

print('1961-1990 -> Köppen:', koppen_antes['classe'], '| Thornthwaite:', thornthwaite_antes['classe'])
```

Agora **escreva você** o bloco de 1991–2020, seguindo o modelo acima. Use os nomes `temperatura_depois`,
`chuva_depois`, `koppen_depois`, `etp_depois` e `thornthwaite_depois`.

```python
# ---------- 1991-2020 ----------
# (escreva aqui, seguindo o modelo do bloco de 1961-1990)
```

---

## Semana 3: a tabela das folgas, antes × depois

Este é o **primeiro resultado de pesquisa** de verdade.

```python
# Folgas de 1961-1990 (uma por linha, como na Missão 2)
folga_A_antes = min(temperatura_antes) - 18
folga_a_antes = max(temperatura_antes) - 22
folga_f_antes = min(chuva_antes) - 60
im_antes = thornthwaite_antes['Im']
etp_anual_antes = thornthwaite_antes['ETP_anual']

# Folgas de 1991-2020
folga_A_depois = min(temperatura_depois) - 18
folga_a_depois = max(temperatura_depois) - 22
folga_f_depois = min(chuva_depois) - 60
im_depois = thornthwaite_depois['Im']
etp_anual_depois = thornthwaite_depois['ETP_anual']

# Monta a tabela: cada coluna é um período, cada linha é um critério
tabela = pd.DataFrame({
    '1961-1990': [folga_A_antes, folga_a_antes, folga_f_antes, im_antes, etp_anual_antes],
    '1991-2020': [folga_A_depois, folga_a_depois, folga_f_depois, im_depois, etp_anual_depois],
}, index=['Folga A/C (°C)', 'Folga a/b (°C)', 'Folga Af (mm)', 'Im (%)', 'ETP anual (mm)'])

# Coluna da diferença: depois menos antes
tabela['Diferença'] = tabela['1991-2020'] - tabela['1961-1990']

# Salva a tabela em CSV (abre no Excel)
tabela.round(2).to_csv(f'{BASE}/resultados/duas_normais_santa_helena.csv')

tabela.round(2)
```

> 🧠 **Interprete cada linha da coluna "Diferença".** A folga ficou mais perto de zero ou mais longe?
> Ex.: se a folga A/C era −1,4 e foi para −0,9, o mês mais frio esquentou 0,5 °C e o clima ficou **mais
> perto** de virar tropical.

### Desafio opcional: a folga do grupo B

Este desafio apresenta o `if` ("se"), que você vai usar de verdade na Missão 9. Programe o limiar de aridez
da Missão 2:

```python
# Chuva do verão (out, nov, dez, jan, fev, mar).
# Nas listas, a posição começa em 0: jan = [0], fev = [1], ..., dez = [11].
chuva_verao = chuva_antes[9] + chuva_antes[10] + chuva_antes[11] + chuva_antes[0] + chuva_antes[1] + chuva_antes[2]

# Fração da chuva anual que cai no verão
fracao_verao = chuva_verao / sum(chuva_antes)

# Temperatura média anual
temperatura_media_antes = sum(temperatura_antes) / 12

# O limiar depende de QUANDO chove. "if" quer dizer "se"; "elif", "senão, se"; "else", "senão".
if fracao_verao >= 0.7:
    limiar_B = 10 * (2 * temperatura_media_antes + 28)
elif fracao_verao <= 0.3:
    limiar_B = 10 * (2 * temperatura_media_antes)
else:
    limiar_B = 10 * (2 * temperatura_media_antes + 14)

folga_B_antes = sum(chuva_antes) - limiar_B
print('Folga B (mm):', round(folga_B_antes))
```

> ⚠️ Repare nos **quatro espaços** antes das linhas de dentro do `if`. No Python, esse recuo diz quais linhas
> pertencem ao `if`. Se tirar os espaços, dá erro.

---

## 📦 Entregável

- ✍️ A seção **Sua vez** do notebook de exemplo, feita para as capitais pedidas.
- A figura `duas_normais_santa_helena.png`.
- O arquivo `resultados/duas_normais_santa_helena.csv`.
- Um parágrafo (5 a 8 linhas) respondendo: **o clima de Santa Helena mudou entre as duas normais? A classe
  mudou? As folgas diminuíram?**

## 🗣️ Para o próximo encontro, saiba responder

- O que faz `groupby(periodo.index.month).mean()`?
- Por que os dois períodos são independentes?
- Qual critério mais se aproximou do limiar?

## ✅ Checklist

- [ ] Calculei as duas normais a partir da série
- [ ] Fiz o climograma comparativo
- [ ] Classifiquei os dois períodos (escrevi o bloco de 1991–2020 sozinha)
- [ ] Montei e salvei a tabela de folgas
- [ ] Escrevi o parágrafo de interpretação
- [ ] Preenchi o diário de bordo
