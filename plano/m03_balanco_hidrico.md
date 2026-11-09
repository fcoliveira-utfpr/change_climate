# Missão 3: O balanço hídrico, ou quanta água sobra e quanta falta

> **Pergunta da missão:** em que meses sobra água no solo de Santa Helena, e em quais falta?
> **Duração:** 3 semanas
> **Notebook:** `m03_balanco_hidrico.ipynb`
> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com)
> 📓 **Notebook de exemplo:** [Exemplo 04: Balanço hídrico (abrir no Colab)](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/04_balanco_hidrico.ipynb). O exemplo é feito para Santa Helena (e Curitiba); na seção ✍️ **Sua vez**, você repete para as capitais.

---

## Por que isso importa

O Köppen olha só a chuva e a temperatura. Mas, para as plantas e o solo, o que importa é a **água
disponível**: a chuva que cai **menos** a água que a atmosfera "puxa" de volta (a **evapotranspiração**).

A classificação de **Thornthwaite**, que você vai fazer na Missão 4, é baseada nesse balanço. Por isso,
antes, você precisa entendê-lo.

**Conceitos (leia no Pereira, Angelocci e Sentelhas, capítulo de balanço hídrico):**

- **ETP (evapotranspiração potencial):** quanto de água evaporaria de uma área com grama, se nunca faltasse
  água. Depende principalmente da **temperatura**.
- **CAD (capacidade de água disponível):** o tamanho da "caixa d'água" do solo. Vamos usar **100 mm**.
- **EXC (excedente):** quando a chuva enche a caixa e transborda. A água sobra.
- **DEF (deficiência):** quando a caixa esvazia e a planta não consegue toda a água de que precisa. A água
  falta.

## O que você vai aprender de Python

- **tabela (`DataFrame`):** como uma planilha do Excel, com linhas e colunas;
- **coluna:** pegar uma coluna da tabela pelo nome (`tabela['ETP_mm_mes']`).

---

## Semana 1: montar a tabela do clima

```python
# Instala e carrega as bibliotecas
!pip install agrometeorologiapy
import agrometeorologiapy as amp
import pandas as pd                # pandas é a biblioteca das tabelas
import matplotlib.pyplot as plt
```

```python
# Dados de Santa Helena (os mesmos das missões anteriores)
latitude = -24.86
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
temperatura = [___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___]
chuva = [___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___]

# Monta uma tabela com 3 colunas.
# À esquerda dos dois-pontos, o NOME da coluna; à direita, a lista de valores.
clima = pd.DataFrame({
    'Meses': meses,
    'T_media_C': temperatura,
    'P (mm/mês)': chuva,
})

# Mostra a tabela
clima
```

> 💡 Quando a **última linha** de uma célula é só o nome de uma tabela, o Colab mostra a tabela formatada.

Experimente:

```python
# Pega uma coluna só, pelo nome
clima['T_media_C']
```

```python
# Média de uma coluna
clima['T_media_C'].mean()
```

---

## Semana 2: a ETP e o balanço

### ETP de Thornthwaite

```python
# Calcula a ETP mensal pelo método de Thornthwaite.
# A função recebe a tabela e a latitude e devolve a MESMA tabela
# com uma coluna nova, chamada 'ETP_mm_mes'.
clima = amp.thornthwaite_mensal(clima, lat=latitude)

clima
```

> 🧠 **Preveja antes de olhar:** em qual mês a ETP vai ser maior? Por quê?

### Balanço hídrico

A função do balanço precisa de uma coluna chamada exatamente `'ETP (mm/mês)'`. Então copiamos a coluna da
ETP com esse nome:

```python
# Cria uma coluna nova, com o nome que a função do balanço espera,
# copiando os valores da coluna 'ETP_mm_mes'
clima['ETP (mm/mês)'] = clima['ETP_mm_mes']

# Calcula o balanço hídrico climatológico (Thornthwaite & Mather, 1955)
# com uma "caixa d'água" de 100 mm
balanco = amp.balanco_hidrico_climatologico(clima, CAD=100)

balanco
```

A tabela do balanço tem várias colunas. As mais importantes para nós:

| Coluna | Significado |
|---|---|
| `P-ETP` | chuva menos ETP; negativo indica que a atmosfera pede mais água do que chove |
| `ARM (mm/mês)` | água armazenada no solo no fim do mês |
| `ETR (mm/mês)` | evapotranspiração real (a que de fato aconteceu) |
| `DEF (mm/mês)` | deficiência hídrica |
| `EXC (mm/mês)` | excedente hídrico |

```python
# Totais do ano
deficiencia_anual = balanco['DEF (mm/mês)'].sum()
excedente_anual = balanco['EXC (mm/mês)'].sum()
etp_anual = balanco['ETP (mm/mês)'].sum()

print('ETP anual (mm):', round(etp_anual))
print('Deficiência anual (mm):', round(deficiencia_anual))
print('Excedente anual (mm):', round(excedente_anual))
```

---

## Semana 3: o gráfico do balanço

```python
# Cria a figura
fig, eixo = plt.subplots(figsize=(9, 4))

# Excedente: barras azuis para CIMA
eixo.bar(meses, balanco['EXC (mm/mês)'], color='steelblue', label='Excedente')

# Deficiência: barras laranja para BAIXO (por isso o sinal de menos)
eixo.bar(meses, -balanco['DEF (mm/mês)'], color='orange', label='Deficiência')

# Linha no zero
eixo.axhline(0, color='black')

eixo.set_ylabel('mm/mês')
eixo.set_title('Balanço hídrico de Santa Helena-PR (CAD = 100 mm)')
eixo.legend()     # mostra a legenda com os nomes das barras
plt.show()
```

Salve em `figuras/balanco_hidrico_santa_helena.png`.

### Experimente

1. Troque `CAD=100` por `CAD=50` e depois por `CAD=200`. O que acontece com a deficiência e o excedente?
   Faz sentido?
2. Some 2 °C a todos os meses (digite uma nova lista de temperatura) e refaça o balanço. A deficiência
   aumenta? Por quê?

> 🧠 O experimento 2 já mostra **como o aquecimento afeta a água do solo**, mesmo sem mudar a chuva.

---

## Se der erro

| Mensagem | O que costuma ser |
|---|---|
| `KeyError: 'ETP (mm/mês)'` | o nome da coluna está diferente (acento, espaço, parênteses) |
| `ValueError: ... length` | uma das listas não tem 12 valores |

## 📦 Entregável

- ✍️ A seção **Sua vez** do notebook de exemplo, feita para as capitais pedidas.
- A figura `balanco_hidrico_santa_helena.png`.
- Uma célula de texto com:
  1. os meses com excedente e os meses com deficiência (se houver);
  2. a ETP, a DEF e o EXC anuais;
  3. as respostas dos dois experimentos.

## 🗣️ Para o próximo encontro, saiba responder

- O que é a ETP e por que ela depende da temperatura?
- O que acontece com o excedente se a CAD for maior? Por quê?
- O que é uma "coluna" de um DataFrame?

## ✅ Checklist

- [ ] Montei a tabela do clima
- [ ] Calculei a ETP e o balanço
- [ ] Fiz e salvei o gráfico
- [ ] Fiz os dois experimentos
- [ ] Preenchi o diário de bordo
