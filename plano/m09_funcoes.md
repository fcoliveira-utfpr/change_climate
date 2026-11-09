# Missão 9: A sua própria função, ou o mesmo método para outro lugar

> **Pergunta da missão:** Curitiba está mais perto ou mais longe de mudar de classe que Santa Helena?
> **Duração:** 3 semanas
> **Notebook:** `m08_funcoes.ipynb`
> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com)
> 📓 **Notebook de exemplo:** [Exemplo 10: Funções e capitais (abrir no Colab)](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/10_funcoes_e_capitais.ipynb). O exemplo é feito para Santa Helena (e Curitiba); na seção ✍️ **Sua vez**, você repete para as capitais.

---

## Por que isso importa

O código da Missão 8 funciona para Santa Helena. Para fazer o mesmo em Curitiba, você poderia copiar tudo e
trocar o nome do arquivo... e depois copiar de novo para cada cidade. Isso gera erros e dá muito trabalho.

A solução é transformar o código numa **função**: um bloco com nome, que recebe dados (a série e a latitude)
e devolve um resultado (a tabela). Depois, basta **chamar** a função para cada lugar.

**Curitiba** é um bom teste: nos mapas clássicos, o clima é **Cfb** (verão ameno), mas a temperatura do mês
mais quente fica perto de 22 °C, o limiar entre **b** e **a**. Será que ela está virando Cfa?

## O que você vai aprender de Python

- **criar uma função** com `def` e devolver um resultado com `return`;
- **decidir** com `if` (que você conheceu no desafio da Missão 7).

---

## Semana 1: a primeira função

### Uma função pequena, para entender

```python
# "def" cria uma função. Aqui, o nome dela é folga_A_C.
# Entre parênteses fica o que ela RECEBE: uma lista de 12 temperaturas.
def folga_A_C(temperatura):
    # Tudo o que está recuado pertence à função.
    t_mes_frio = min(temperatura)
    folga = t_mes_frio - 18
    # "return" devolve o resultado para quem chamou a função
    return folga


# Usando a função com uma lista de exemplo
exemplo = [25, 25, 24, 22, 19, 17, 16.5, 18, 20, 22, 24, 25]
print(folga_A_C(exemplo))      # deve mostrar -1.5
```

> 🧠 Mude a lista `exemplo` e chame a função de novo. Você não precisou reescrever a conta.

### Uma função que encontra o limite mais próximo

Na Missão 4, você achou à mão os limites de Im. Agora a função faz isso sozinha:

```python
# Limites de classe de Thornthwaite (os mesmos da biblioteca)
LIMITES_IM = [-40, -20, 0, 20, 40, 60, 80, 100]                 # umidade, em %
LIMITES_ETP = [142, 285, 427, 570, 712, 855, 997, 1140]        # térmica, em mm


def folga_mais_proxima(valor, limites):
    """
    Distância entre "valor" e o limite de classe mais próximo dele.
    Exemplo: valor = 72.4 e limites de Im -> o mais próximo é 80, a folga é 7.6.
    """
    # Começamos com um número bem grande, que qualquer distância real vai superar
    menor_distancia = 99999

    # Olha cada limite, um de cada vez
    for limite in limites:
        # abs() tira o sinal: a distância é sempre positiva
        distancia = abs(valor - limite)

        # Se esta distância for menor que a menor encontrada até agora, guarda ela
        if distancia < menor_distancia:
            menor_distancia = distancia

    return menor_distancia


# Teste: o resultado deve ser 7.6
print(folga_mais_proxima(72.4, LIMITES_IM))
```

> 🧠 **Teste com valores que você sabe a resposta:** Im = 59 (deve dar 1), ETP = 1000 (deve dar 3).

---

## Semana 2: a função do clima de um período

Esta função junta **tudo** o que você fez nas Missões 6 e 7 para **uma janela**:

```python
!pip install agrometeorologiapy
import agrometeorologiapy as amp
import pandas as pd


def clima_de_um_periodo(serie, primeiro_ano, ultimo_ano, latitude):
    """
    Calcula a normal de um período e devolve a classe e as folgas.

    Recebe:
        serie        -> tabela mensal com as colunas 'tmed' e 'chuva'
        primeiro_ano -> primeiro ano do período (ex.: 1961)
        ultimo_ano   -> último ano do período (ex.: 1990)
        latitude     -> latitude do local, em graus
    Devolve:
        um dicionário com as classes e as folgas
    """
    # 1) Recorta o período e calcula a normal (média de cada mês)
    janela = serie.loc[str(primeiro_ano):str(ultimo_ano)]
    normal = janela.groupby(janela.index.month).mean()
    temperatura = normal['tmed'].tolist()
    chuva = normal['chuva'].tolist()
    chuva_anual = sum(chuva)

    # 2) Köppen
    koppen = amp.classificacao_koppen(temperatura, chuva, latitude)

    # 3) Thornthwaite
    tabela_etp = amp.thornthwaite_mensal(pd.DataFrame({'T_media_C': temperatura}), lat=latitude)
    etp = tabela_etp['ETP_mm_mes']
    thornthwaite = amp.classificacao_thornthwaite(chuva, etp, latitude)

    # 4) Folgas de Köppen
    folga_A = min(temperatura) - 18
    folga_a = max(temperatura) - 22
    folga_f = min(chuva) - 60
    folga_m = min(chuva) - (100 - chuva_anual / 25)

    # 5) Folgas de Thornthwaite
    folga_Im = folga_mais_proxima(thornthwaite['Im'], LIMITES_IM)
    folga_ETP = folga_mais_proxima(thornthwaite['ETP_anual'], LIMITES_ETP)

    # 6) Junta tudo num dicionário e devolve
    resultado = {
        'periodo': str(primeiro_ano) + '-' + str(ultimo_ano),
        'koppen': koppen['classe'],
        'thornthwaite': thornthwaite['classe'],
        'folga_A': folga_A,
        'folga_a': folga_a,
        'folga_f': folga_f,
        'folga_m': folga_m,
        'Im': thornthwaite['Im'],
        'folga_Im': folga_Im,
        'ETP_anual': thornthwaite['ETP_anual'],
        'folga_ETP': folga_ETP,
    }
    return resultado
```

Teste com a normal 1961–1990 de Santa Helena. O resultado tem de ser igual ao da Missão 7:

```python
from google.colab import drive
drive.mount('/content/drive')

BASE = '/content/drive/MyDrive/mudanca_climatica_br'
serie_sh = pd.read_csv(f'{BASE}/dados/santa_helena_mensal.csv', parse_dates=['data'], index_col='data')

clima_de_um_periodo(serie_sh, 1961, 1990, -24.86)
```

---

## Semana 3: a função da janela móvel e Curitiba

### A função que analisa um ponto inteiro

```python
def analisar_ponto(serie, latitude, primeiro=1990, ultimo=2025):
    """
    Clima de referência móvel: para cada ano, a normal dos 30 anos que terminam nele.
    Devolve uma tabela com uma linha por ano.
    (primeiro=1990 quer dizer: se você não informar, usa 1990)
    """
    linhas = []
    for ano in range(primeiro, ultimo + 1):
        # Usa a função da semana 2 para a janela que termina em "ano"
        linha = clima_de_um_periodo(serie, ano - 29, ano, latitude)
        # Acrescenta o ano ao dicionário
        linha['ano'] = ano
        linhas.append(linha)

    tabela = pd.DataFrame(linhas)
    tabela = tabela.set_index('ano')
    return tabela
```

Agora, **duas linhas** fazem tudo o que a Missão 8 fazia:

```python
resultado_sh = analisar_ponto(serie_sh, -24.86)
resultado_sh.round(2)
```

> 🧠 **Confira:** `resultado_sh` é igual à tabela da Missão 8?

### Curitiba

O arquivo `curitiba_mensal.csv` está na pasta `dados/` (é o mesmo que você extrairia para PR na Missão 5). A latitude de Curitiba é cerca de **−25,43**.

```python
serie_ctba = pd.read_csv(f'{BASE}/dados/___', parse_dates=['data'], index_col='data')
resultado_ctba = analisar_ponto(serie_ctba, ___)

resultado_ctba.round(3).to_csv(f'{BASE}/resultados/janela_movel_curitiba.csv')
resultado_ctba.round(2)
```

### O gráfico das duas cidades

Faça você mesma um gráfico com **a folga a/b das duas cidades** no mesmo eixo (uma linha para cada cidade,
com legenda e a linha do zero). Use como modelo o gráfico da Missão 7 (duas linhas no mesmo eixo) e o da
Missão 8 (folga no tempo).

---

## 📦 Entregável

- ✍️ A seção **Sua vez** do notebook de exemplo, feita para as capitais pedidas.
- O notebook com as três funções (`folga_mais_proxima`, `clima_de_um_periodo`, `analisar_ponto`), cada uma
  testada.
- `resultados/janela_movel_curitiba.csv`.
- A figura das folgas a/b das duas cidades.
- Um parágrafo: **Curitiba está virando Cfa? Qual das duas cidades está mais perto de mudar de classe, e em
  qual critério?**

## 🗣️ Para o próximo encontro, saiba responder

- O que é uma função? O que fazem `def` e `return`?
- Explique, linha a linha, a função `folga_mais_proxima`.
- Qual a vantagem de ter a função `analisar_ponto`?

## ✅ Checklist

- [ ] Criei e testei `folga_A_C` e `folga_mais_proxima`
- [ ] Criei `clima_de_um_periodo` e conferi com a Missão 7
- [ ] Criei `analisar_ponto` e conferi com a Missão 8
- [ ] Analisei Curitiba
- [ ] Fiz o gráfico das duas cidades sozinha
- [ ] Preenchi o diário de bordo
