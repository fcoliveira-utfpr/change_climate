# Capítulo 3 — Python Essencial para o Projeto

> **Objetivo do capítulo:** aprender só o Python que será usado no projeto, sempre com exemplos climáticos.
> Crie o notebook `cap03_python.ipynb` e digite (não copie) os exemplos.

---

## 3.1 Variáveis e tipos

Uma variável guarda um valor com um nome.

```python
cidade = 'Santa Helena'      # texto (str)
latitude = -24.86            # número decimal (float)
ano_inicio = 1961            # número inteiro (int)
tem_dados = True             # verdadeiro/falso (bool)

print(cidade, latitude, ano_inicio)
print(type(latitude))
```

Operações:

```python
tmax = 31.2
tmin = 19.8
tmed = (tmax + tmin) / 2
print(f'Temperatura média: {tmed:.1f} °C')   # f-string: formata o texto
```

> 💡 O `f'...'` permite colocar variáveis dentro do texto. `:.1f` = uma casa decimal.

---

## 3.2 Listas

Guardam vários valores em ordem. Muito úteis para séries mensais.

```python
chuva_mensal = [180, 165, 130, 150, 140, 110, 90, 85, 130, 190, 170, 185]   # mm

print(chuva_mensal[0])     # janeiro (o índice começa em 0!)
print(chuva_mensal[-1])    # dezembro (último)
print(chuva_mensal[0:3])   # jan, fev, mar
print(len(chuva_mensal))   # 12
print(sum(chuva_mensal))   # total anual
print(min(chuva_mensal))   # mês mais seco
```

> ⚠️ Em Python, a contagem começa em **0**. Janeiro é o índice 0; dezembro, o 11.

---

## 3.3 Dicionários

Guardam pares **chave → valor**. Perfeitos para descrever um ponto.

```python
ponto = {
    'uf': 'PR',
    'municipio': 'Curitiba',
    'lat': -25.43,
    'lon': -49.27
}

print(ponto['municipio'])
print(ponto['lat'], ponto['lon'])
```

---

## 3.4 Condicionais (`if`)

Toda classificação climática é feita de condições. Exemplo simplificado de Köppen:

```python
t_mes_mais_frio = 14.5   # °C

if t_mes_mais_frio >= 18:
    grupo = 'A'   # tropical
else:
    grupo = 'C'   # temperado (simplificado: ignora o grupo B, de clima seco)

print('Grupo Köppen:', grupo)
```

```python
p_mes_mais_seco = 45   # mm

if p_mes_mais_seco >= 60:
    print('Sem estação seca definida')
elif p_mes_mais_seco >= 30:
    print('Estação seca moderada')
else:
    print('Estação seca marcante')
```

> ⚠️ A **indentação** (os 4 espaços) faz parte da linguagem. Errar o recuo gera erro.

---

## 3.5 Laços (`for`)

Repetem uma tarefa. É assim que vamos passar pelos anos e pelos 27 pontos.

```python
meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun',
         'jul', 'ago', 'set', 'out', 'nov', 'dez']

for i in range(12):
    print(meses[i], chuva_mensal[i], 'mm')
```

Percorrendo anos e montando as janelas de 30 anos (a lógica central do projeto!):

```python
for ano in range(1990, 1996):
    inicio = ano - 29
    print(f'Clima de {ano}: usa {inicio} a {ano}')
```

> 🧠 Pare e confira: por que `ano - 29` e não `ano - 30`? Conte os anos de 1961 a 1990.

Percorrendo uma lista de dicionários (como faremos com os 27 pontos):

```python
pontos = [
    {'uf': 'PR', 'lat': -25.43, 'lon': -49.27},
    {'uf': 'SP', 'lat': -23.55, 'lon': -46.63},
]

for p in pontos:
    print(p['uf'], p['lat'], p['lon'])
```

---

## 3.6 Funções

Uma função é um bloco de código com nome, que recebe entradas e devolve um resultado. **É a habilidade mais importante deste projeto**: o código da Fase A só será reaproveitado na Fase B se estiver em funções.

```python
def temperatura_media(tmax, tmin):
    """Calcula a temperatura média diária (°C)."""
    return (tmax + tmin) / 2

print(temperatura_media(31.2, 19.8))
```

```python
def janela_30_anos(ano):
    """Retorna o ano inicial e final da janela de 30 anos que termina em `ano`."""
    return ano - 29, ano

ini, fim = janela_30_anos(2000)
print(ini, fim)   # 1971 2000
```

**Boas práticas para funções:**
- Nome que diga o que ela faz (`calcular_chuva_anual`, não `f1`).
- Uma *docstring* (`"""..."""`) explicando entradas e saída.
- Cada função faz **uma** coisa.

---

## 3.7 Exercícios

1. Com a lista `chuva_mensal`, calcule o total anual e descubra **qual mês** é o mais seco (dica: `chuva_mensal.index(min(chuva_mensal))`).
2. Crie a lista `temp_mensal` com 12 temperaturas inventadas e encontre o mês mais frio e o mais quente.
3. Escreva a função `grupo_koppen_simples(t_mes_mais_frio)` que retorna `'A'` ou `'C'`.
4. Com um `for`, imprima as janelas de 30 anos de **todos** os anos entre 1990 e 2020.
5. Crie uma lista com 3 pontos (dicionários) de capitais que você conhece e imprima-os com um `for`.

---

## 3.8 Pandas: tabelas de dados

O `pandas` organiza dados em **DataFrames** (tabelas com linhas e colunas). Toda a análise do projeto será feita com ele.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'mes': ['jan', 'fev', 'mar'],
    'chuva': [180, 165, 130],
    'tmed': [25.1, 24.8, 23.9]
})

df
```

Comandos básicos de exploração:

```python
df.head()               # primeiras linhas
df.info()               # tipos das colunas e valores faltantes
df.describe()           # estatísticas resumidas
df['chuva']             # uma coluna
df['chuva'].sum()       # soma da coluna
df[df['chuva'] > 150]   # filtro: meses com mais de 150 mm
```

Criando uma coluna nova:

```python
df['chuva_cm'] = df['chuva'] / 10
```

---

## 3.9 Baixando dados reais: base do Xavier (receita pronta)

Vamos treinar com os dados **reais do projeto**: a série diária do Xavier para Santa Helena-PR.
O código abaixo usa o Google Earth Engine. **Não se preocupe em entendê-lo agora**: ele será explicado no Capítulo 5. Por enquanto, basta rodar.

```python
import ee

ee.Initialize(project='ee-seunome')   # seu ID de projeto (Capítulo 2)

# Coleções do Xavier (BR-DWGD) — conferir nomes no catálogo
COLECOES = {
    'chuva': 'projects/sat-io/open-datasets/BR-DWGD/PR',
    'tmax':  'projects/sat-io/open-datasets/BR-DWGD/TMAX',
    'tmin':  'projects/sat-io/open-datasets/BR-DWGD/TMIN',
}

lat, lon = -24.86, -54.33                 # Santa Helena-PR
ponto = ee.Geometry.Point([lon, lat])     # GEE: [lon, lat]

def extrair_variavel(colecao_id, ano_ini, ano_fim):
    """Extrai a série diária de uma variável no ponto, década a década."""
    partes = []
    for ini in range(ano_ini, ano_fim + 1, 10):
        fim = min(ini + 9, ano_fim)
        col = (ee.ImageCollection(colecao_id)
               .filterDate(f'{ini}-01-01', f'{fim + 1}-01-01')
               .select([0]))                        # primeira (única) banda
        linhas = col.getRegion(ponto, 10000).getInfo()
        partes.append(pd.DataFrame(linhas[1:], columns=linhas[0]))
    tab = pd.concat(partes)
    serie = pd.Series(tab.iloc[:, 4].astype(float).values,
                      index=pd.to_datetime(tab['time'], unit='ms'))
    return serie.sort_index()

df = pd.DataFrame({
    nome: extrair_variavel(cid, 1961, 2020)
    for nome, cid in COLECOES.items()
})
df.index.name = 'data'
df.head()
```

| Coluna | Significado | Unidade |
|---|---|---|
| `chuva` | precipitação diária | mm |
| `tmax` | temperatura máxima | °C |
| `tmin` | temperatura mínima | °C |

> ⏳ A extração pode levar alguns minutos.
> ⚠️ Confira no catálogo (https://gee-community-catalog.org/projects/br_dwgd/) os nomes das coleções e o último ano disponível; ajuste `2020` se houver dados mais recentes.

Salve imediatamente no Drive, para não precisar baixar de novo:

```python
df.to_csv(f'{BASE}/dados/xavier_santa_helena_diario.csv')
```

Nas próximas sessões, basta ler o arquivo:

```python
df = pd.read_csv(f'{BASE}/dados/xavier_santa_helena_diario.csv',
                 index_col='data', parse_dates=True)
```

---

## 3.10 Datas: o índice temporal

O índice da tabela está em formato de **data**, o que permite filtrar períodos facilmente:

```python
df.loc['2000']                      # só o ano 2000
df.loc['1971-01-01':'2000-12-31']   # um intervalo
```

> 💡 Esse filtro por intervalo é exatamente o que usaremos para recortar as janelas de 30 anos.

Calcule a temperatura média diária e verifique se há falhas:

```python
df['tmed'] = (df['tmax'] + df['tmin']) / 2
df.isna().sum()   # quantidade de dias sem dado em cada coluna
```

> 🧠 Confira também se os valores fazem sentido: `df.describe()`. Chuva negativa ou temperatura de 60 °C indicam problema.

---

## 3.11 Agregação: de diário para mensal e anual

Regra fundamental do projeto:
- **Precipitação → SOMA** (total de chuva no mês)
- **Temperatura → MÉDIA** (temperatura média do mês)

```python
mensal = pd.DataFrame({
    'chuva': df['chuva'].resample('MS').sum(),
    'tmed': df['tmed'].resample('MS').mean()
})

anual = pd.DataFrame({
    'chuva': df['chuva'].resample('YS').sum(),
    'tmed': df['tmed'].resample('YS').mean()
})

mensal.head()
```

> ⚠️ Somar temperatura ou tirar média de chuva diária para obter o mês são erros clássicos. Sempre confira.

### Médias mensais de um período (a base do clima)

O clima de um período tem **12 valores**: a média de todos os janeiros, de todos os fevereiros etc.

```python
periodo = mensal.loc['1971':'2000']
clima = periodo.groupby(periodo.index.month).mean()
clima.index.name = 'mes'
clima
```

> 🧠 A chuva de `clima` é a **média dos totais mensais** (ex.: média dos 30 janeiros), e não a soma deles.

---

## 3.12 Gráficos com matplotlib

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(anual.index.year, anual['tmed'], marker='o')
ax.set_xlabel('Ano')
ax.set_ylabel('Temperatura média (°C)')
ax.set_title('Temperatura média anual — Santa Helena-PR (Xavier)')
ax.grid(alpha=0.3)
plt.show()
```

### Climograma (chuva em barras + temperatura em linha)

```python
meses = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']

fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar(meses, clima['chuva'], color='steelblue')
ax1.set_ylabel('Precipitação (mm)')

ax2 = ax1.twinx()
ax2.plot(meses, clima['tmed'], color='red', marker='o')
ax2.set_ylabel('Temperatura (°C)')

plt.title('Climograma 1971–2000 — Santa Helena-PR (Xavier)')
plt.show()
```

Salvando figuras e tabelas no Drive:

```python
fig.savefig(f'{BASE}/figuras/climograma_santa_helena.png', dpi=300, bbox_inches='tight')
mensal.to_csv(f'{BASE}/dados/xavier_santa_helena_mensal.csv')
```

---

## 3.13 Juntando tudo: as primeiras funções do projeto

```python
def janela_30_anos(ano):
    """Retorna o ano inicial e final da janela de 30 anos que termina em `ano`."""
    return ano - 29, ano


def clima_do_periodo(mensal, ano_ini, ano_fim):
    """Retorna as 12 médias mensais (chuva e tmed) entre ano_ini e ano_fim."""
    periodo = mensal.loc[str(ano_ini):str(ano_fim)]
    return periodo.groupby(periodo.index.month).mean()


ini, fim = janela_30_anos(2000)
clima_2000 = clima_do_periodo(mensal, ini, fim)   # 1971–2000
clima_2000
```

> 💡 Essas duas funções são o coração do método. No Capítulo 7 elas serão usadas para calcular o clima de **todos** os anos e classificá-los.

---

## 3.14 Exercícios (Parte 2)

1. Calcule o total anual de chuva e identifique o ano mais chuvoso e o mais seco.
2. Faça o gráfico de chuva anual em barras.
3. Faça os climogramas de 1961–1990 e de 1991–2020 e compare: o que mudou?
4. Use `janela_30_anos` e `clima_do_periodo` dentro de um `for` para calcular o clima de cada ano de 1990 a 2020. Guarde a temperatura média anual de cada clima (média dos 12 meses) e a chuva anual (soma dos 12 meses) e faça um gráfico da evolução.
5. Salve o CSV mensal e os climogramas no Drive.

---

## ✅ Checklist do Capítulo 3

- [ ] Digitei e rodei todos os exemplos da Parte 1
- [ ] Baixei a série do Xavier para Santa Helena e salvei no Drive
- [ ] Verifiquei falhas com `isna()` e valores estranhos com `describe()`
- [ ] Agreguei corretamente: chuva = soma; temperatura = média
- [ ] Calculei as 12 médias mensais de um período com `groupby`
- [ ] Fiz o gráfico anual e os climogramas
- [ ] Criei e usei as funções `janela_30_anos` e `clima_do_periodo`
- [ ] Respondi os exercícios das Partes 1 e 2

**Entregável 3:** notebook `cap03_python.ipynb` rodando do início ao fim + `xavier_santa_helena_mensal.csv` + climogramas em PNG.
