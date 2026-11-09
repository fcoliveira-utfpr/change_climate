# Missão 5: Buscar os próprios dados no Google Earth Engine

> **Pergunta da missão:** de onde vêm os dados que usei até agora? Consigo buscá-los sozinha, para qualquer
> lugar do Brasil?
> **Duração:** 3 semanas
> **Notebook:** `m05_gee.ipynb`
> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com) · 🌎 [Earth Engine Code Editor](https://code.earthengine.google.com)
> 📓 **Notebook de exemplo:** [Exemplo 06: Extrair dados no GEE (abrir no Colab)](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/06_extrair_dados_gee.ipynb). O exemplo é feito para Santa Helena (e Curitiba); na seção ✍️ **Sua vez**, você repete para as capitais.
> **Início da fase 2:** os dados e o tempo

---

## Por que isso importa

Na fase 1, você usou **uma** normal (12 temperaturas e 12 chuvas) de Santa Helena e as normais das capitais
do INMET. Daqui para frente, vamos precisar da **série completa**: um valor por mês, de 1961 a 2025.

Esses dados vêm da **base do Xavier**, guardada no **Google Earth Engine (GEE)**, uma plataforma do Google que
guarda e processa dados geográficos na nuvem. A base tem **um mapa por dia**, de 1961 a 2025, para o Brasil
inteiro: são mais de 23 mil mapas. Ninguém baixa isso para o próprio computador. Pedimos ao GEE só o
**pedaço** que interessa, ou seja, um ponto.

Nesta missão você vai:
1. criar o seu próprio projeto no GEE;
2. extrair a série de **Santa Helena** e **conferir** se ela é igual à do arquivo do projeto;
3. **repetir** a extração para as **27 capitais**. Esses são os dados que você vai usar no resto da pesquisa.

Depois disso, você consegue buscar os dados de **qualquer** lugar do Brasil sozinha.

## O que você vai aprender de Python

- **autenticar** num serviço na nuvem;
- usar um **bloco de código pronto e longo**, entendendo o que cada parte faz, sem precisar escrevê-lo do
  zero. Isso é muito comum na pesquisa.

> ⚠️ **Esta é a missão com mais chance de travar por configuração** (conta, projeto, permissões). Não é
> falta de capacidade sua: acontece com todo mundo. A semana 1 é feita **junto com o orientador**, no
> encontro.

---

## Semana 1: criar o projeto no Earth Engine (sem código, junto com o orientador)

O GEE é **gratuito para pesquisa e ensino** (uso "não comercial"). Para usá-lo, você precisa de um
**projeto** no Google Cloud, registrado no Earth Engine. Um projeto é como uma "conta de trabalho": ele tem um
nome único, o **ID do projeto**, que vai aparecer no seu código.

### Passo a passo

1. 🔑 **Entre com a sua conta Google**, a mesma que você usa no Drive e no Colab.
2. 🌎 **Abra a página de cadastro:** **[clique aqui para registrar um projeto no Earth Engine](https://code.earthengine.google.com/register)**.
3. 🎓 **Escolha o uso não comercial:** quando perguntarem o tipo de uso, escolha a opção de **uso não comercial**
   (pesquisa acadêmica / educação). Informe a instituição: **Universidade Tecnológica Federal do Paraná (UTFPR)**.
4. ➕ **Crie um projeto novo:** escolha **criar um novo projeto do Google Cloud**. Dê um ID simples, só com
   letras minúsculas, números e hífen, por exemplo `ee-seunome-utfpr`.
5. ✍️ **Anote o ID do projeto** no diário de bordo. Atenção: é o **ID** (ex.: `ee-seunome-utfpr`), não o
   "nome de exibição".
6. 🆓 **Nível de uso:** se perguntarem, escolha o **Community Tier** (o gratuito, que não pede cartão). Ele
   tem uma cota mensal de processamento muito maior do que vamos usar.
7. ✅ **Confira:** abra o **[Code Editor](https://code.earthengine.google.com)**. Se abrir uma tela com um
   mapa e um editor de código, sem pedir cadastro, deu certo.

> 💡 As telas do Google mudam de tempos em tempos. Se algum botão estiver com outro nome, procure a opção
> mais parecida e anote no diário o que você fez. Assim, a próxima pessoa que usar este guia já sabe.

> 🗓️ Os projetos não comerciais precisam **confirmar o uso não comercial uma vez por ano**. O Google avisa
> por e-mail.

---

## Semana 2: o primeiro contato e a conferência de Santa Helena

### 1. Instalar e autenticar

```python
# Conecta o Drive (como em todas as missões)
from google.colab import drive
drive.mount('/content/drive')
BASE = '/content/drive/MyDrive/mudanca_climatica_br'
```

```python
# Instala a biblioteca do Earth Engine para Python
!pip install earthengine-api
```

```python
import ee
import pandas as pd

# Troque pelo ID do SEU projeto (o que você anotou na semana 1)
PROJETO = '___'

# Abre uma janela para você entrar com a sua conta Google e autorizar o acesso.
# Siga as instruções que aparecerem. Só precisa fazer isso uma vez por sessão do Colab.
ee.Authenticate()

# Conecta ao Earth Engine usando o seu projeto
ee.Initialize(project=PROJETO)

print('Conectada ao Earth Engine!')
```

### 2. Conhecendo a base do Xavier

```python
# Endereço da base do Xavier v3.2.4 no Earth Engine (dados diários, grade de 0,1°)
ASSET_XAVIER = 'projects/ee-alexandrexavier/assets/BR-DWGD'

# Uma "ImageCollection" é uma coleção de imagens: aqui, um mapa para cada dia
colecao = ee.ImageCollection(ASSET_XAVIER)

# Pega a primeira imagem (o primeiro dia)
primeira_imagem = colecao.first()

# Quais variáveis cada mapa diário tem? (cada variável é uma "banda")
print('Variáveis (bandas):', primeira_imagem.bandNames().getInfo())

# Qual é o primeiro dia da base?
data_inicial = ee.Date(primeira_imagem.get('system:time_start')).format('YYYY-MM-dd')
print('Primeiro dia da base:', data_inicial.getInfo())

# Quantos dias (mapas) existem na base?
print('Número de dias na base:', colecao.size().getInfo())
```

> 💡 **Por que `.getInfo()`?** O GEE trabalha "preguiçosamente": ele só calcula quando você pede o
> resultado. O `.getInfo()` é esse pedido: "calcule e me mande a resposta".

> 🧠 **Interprete:** você deve ver as bandas `Tmax`, `Tmin` e `pr` (chuva), entre outras. Procure no artigo
> de Xavier et al. (2022) o que significam `RH`, `Rs`, `u2` e `ET`. E o número de dias, faz sentido para
> 1961 a 2025?

### 3. O bloco de extração (pronto, para ler com atenção)

Este bloco é **longo**, e você **não precisa escrevê-lo**. Copie, cole e **leia todos os comentários**. No
encontro, você vai explicar o que cada uma das três funções faz.

```python
# Período da série
PRIMEIRO_ANO = 1961
ULTIMO_ANO = 2025


def converter_para_unidades_fisicas(imagem):
    """
    Os valores do Xavier são guardados como números inteiros "comprimidos".
    Cada imagem diária traz, nas suas propriedades, o multiplicador (MULT)
    e o deslocamento (ADD) de cada variável:  valor real = valor guardado * MULT + ADD
    """
    # Temperatura máxima do dia, em °C
    tmax = imagem.select('Tmax')
    tmax = tmax.multiply(ee.Number(imagem.get('BAND_Tmax_MULT')))
    tmax = tmax.add(ee.Number(imagem.get('BAND_Tmax_ADD')))

    # Temperatura mínima do dia, em °C
    tmin = imagem.select('Tmin')
    tmin = tmin.multiply(ee.Number(imagem.get('BAND_Tmin_MULT')))
    tmin = tmin.add(ee.Number(imagem.get('BAND_Tmin_ADD')))

    # Chuva do dia, em mm
    chuva = imagem.select('pr')
    chuva = chuva.multiply(ee.Number(imagem.get('BAND_pr_MULT')))
    chuva = chuva.add(ee.Number(imagem.get('BAND_pr_ADD')))

    # Junta as três variáveis numa imagem só e mantém a data do dia
    convertida = ee.Image.cat([tmax, tmin, chuva]).rename(['Tmax', 'Tmin', 'chuva'])
    convertida = convertida.copyProperties(imagem, ['system:time_start'])
    return ee.Image(convertida)


def baixar_dias(latitude, longitude, ano_inicio, ano_fim):
    """
    Baixa os valores DIÁRIOS de um ponto, de 1º de janeiro de ano_inicio
    a 31 de dezembro de ano_fim. Devolve uma tabela com uma linha por dia.
    """
    # O ponto, no formato do Earth Engine (atenção: longitude primeiro!)
    ponto = ee.Geometry.Point([longitude, latitude])

    # Seleciona os dias do período e converte para unidades físicas
    colecao = ee.ImageCollection(ASSET_XAVIER)
    colecao = colecao.filterDate(f'{ano_inicio}-01-01', f'{ano_fim + 1}-01-01')
    colecao = colecao.map(converter_para_unidades_fisicas)

    # getRegion devolve uma lista de linhas: a primeira linha é o cabeçalho
    # (id, longitude, latitude, time, Tmax, Tmin, chuva), as outras são os dias
    linhas = colecao.getRegion(ponto, scale=1000).getInfo()
    cabecalho = linhas[0]
    dias = linhas[1:]

    tabela = pd.DataFrame(dias, columns=cabecalho)

    # A coluna 'time' vem em milissegundos desde 1970; transforma em data
    tabela['data'] = pd.to_datetime(tabela['time'], unit='ms')
    tabela = tabela[['data', 'Tmax', 'Tmin', 'chuva']]
    return tabela


def serie_mensal_do_ponto(latitude, longitude):
    """
    Baixa a série diária inteira, de 10 em 10 anos (para não pedir dados demais
    de uma vez ao Earth Engine), e agrega em meses.
    """
    # Baixa os dias, uma década por vez, e guarda cada pedaço numa lista
    pedacos = []
    for ano_inicio in range(PRIMEIRO_ANO, ULTIMO_ANO + 1, 10):
        ano_fim = min(ano_inicio + 9, ULTIMO_ANO)
        print('   baixando', ano_inicio, 'a', ano_fim)
        pedaco = baixar_dias(latitude, longitude, ano_inicio, ano_fim)
        pedacos.append(pedaco)

    # Junta os pedaços numa tabela só, ordenada pela data
    diaria = pd.concat(pedacos)
    diaria = diaria.sort_values('data')
    diaria = diaria.set_index('data')

    # Temperatura média do dia
    diaria['tmed'] = (diaria['Tmax'] + diaria['Tmin']) / 2

    # Quantos dias tem cada mês, e quantos têm dado
    dias_no_mes = diaria['tmed'].resample('MS').size()
    dias_com_dado_t = diaria['tmed'].resample('MS').count()
    dias_com_dado_p = diaria['chuva'].resample('MS').count()

    # Agrega em meses ('MS' = início do mês): temperatura = média, chuva = soma
    mensal = pd.DataFrame()
    mensal['tmed'] = diaria['tmed'].resample('MS').mean()
    mensal['chuva'] = diaria['chuva'].resample('MS').sum()

    # Apaga os meses incompletos (com algum dia faltando)
    mensal.loc[dias_com_dado_t < dias_no_mes, 'tmed'] = float('nan')
    mensal.loc[dias_com_dado_p < dias_no_mes, 'chuva'] = float('nan')

    mensal.index.name = 'data'
    return mensal.round(2)
```

> 🧠 **Perguntas para o diário (sobre o bloco acima):**
> 1. Por que a temperatura do dia é `(Tmax + Tmin) / 2`?
> 2. Por que o código baixa **de 10 em 10 anos**, e não tudo de uma vez?
> 3. O que acontece com um mês em que falta um dia de dado?

### 4. Extrair Santa Helena e conferir com o arquivo do projeto

```python
# Extrai Santa Helena (leva 1 ou 2 minutos)
serie_minha = serie_mensal_do_ponto(-24.86, -54.33)

# Salva com OUTRO nome, para não apagar o arquivo do projeto
serie_minha.to_csv(f'{BASE}/dados/santa_helena_mensal_minha.csv')
serie_minha.head()
```

```python
# Lê o arquivo do projeto (já está na pasta dados/ do Drive)
serie_projeto = pd.read_csv(f'{BASE}/dados/santa_helena_mensal.csv', parse_dates=['data'], index_col='data')

# Diferença, mês a mês, entre as duas séries.
# abs() tira o sinal; max() pega a maior diferença de todas.
diferenca_temperatura = (serie_minha['tmed'] - serie_projeto['tmed']).abs().max()
diferenca_chuva = (serie_minha['chuva'] - serie_projeto['chuva']).abs().max()

print('Maior diferença de temperatura (°C):', diferenca_temperatura)
print('Maior diferença de chuva (mm):', diferenca_chuva)
```

> ✅ As diferenças devem ser **zero** (ou quase). Se forem, você acabou de **reproduzir** os dados da
> pesquisa, um passo importante em ciência: qualquer pessoa, com o mesmo método, chega ao mesmo dado.

---

## Semana 3: repetir para as 27 capitais

O exemplo da semana 2 foi para **um** lugar. Agora você **repete** o mesmo passo para cada capital.

### 1. Montar a tabela das capitais

Encontre as coordenadas do **centro** de cada capital:

1. 🗺️ Abra o **[Google Maps](https://maps.google.com)** e procure a capital.
2. 🖱️ Clique com o **botão direito** no centro da cidade. O primeiro item do menu são as coordenadas, por
   exemplo `-25.4300, -49.2700`. Clique nelas para copiar.
3. ✍️ O **primeiro** número é a **latitude**; o **segundo**, a **longitude**. Duas casas decimais bastam: a
   grade do Xavier tem pixels de 0,1°.

Digite a tabela no notebook. As duas primeiras linhas são exemplos; complete as outras 25:

```python
# Cada linha é uma capital: sigla do estado, nome, região, latitude e longitude
capitais = pd.DataFrame([
    {'uf': 'PR', 'capital': 'Curitiba', 'regiao': 'Sul', 'lat': -25.43, 'lon': -49.27},
    {'uf': 'DF', 'capital': 'Brasília', 'regiao': 'Centro-Oeste', 'lat': -15.79, 'lon': -47.88},
    # {'uf': '__', 'capital': '___', 'regiao': '___', 'lat': ___, 'lon': ___},
    # ... (complete as 27)
])

# Confira: devem ser 27 linhas
print('Número de capitais:', len(capitais))

# Salva a tabela no Drive, para usar nas próximas missões
capitais.to_csv(f'{BASE}/dados/capitais_27.csv', index=False)
capitais
```

### 2. Repetir a extração, primeiro à mão

Faça **as três primeiras capitais uma por vez**, trocando só as três linhas de cima:

```python
# Troque estas três linhas para cada capital
UF = 'pr'                      # sigla em minúsculas: vira o nome do arquivo
LATITUDE = -25.43
LONGITUDE = -49.27

# O resto é igual para todas as capitais
serie = serie_mensal_do_ponto(LATITUDE, LONGITUDE)
serie.to_csv(f'{BASE}/dados/capitais/{UF}.csv')

# Conferência: quantos meses vieram vazios? (deve ser 0)
print(UF, '-> meses sem temperatura:', serie['tmed'].isna().sum(), '| sem chuva:', serie['chuva'].isna().sum())
```

> 💡 Antes da primeira vez, crie a pasta `capitais` dentro de `dados/` no Drive (botão direito → Nova pasta).

> ⚠️ **Se a série vier toda vazia**, o ponto caiu **no mar**: a grade do Xavier só cobre o continente. Isso
> acontece em capitais do litoral. Mova a coordenada um pouco para o **interior** (por exemplo, 0,05° para
> oeste), anote a mudança na tabela e extraia de novo.

### 3. Repetir para todas, com uma célula pronta

Repetir 27 vezes à mão cansa e dá erro. A célula abaixo faz a **mesma coisa** para cada linha da tabela,
usando o `for`, que você vai aprender de verdade na Missão 8. Por enquanto, leia os comentários e compare
com a célula anterior: é o mesmo código, só que repetido automaticamente.

```python
# 🔧 CÉLULA PRONTA: repete a extração para cada capital da tabela
for indice, capital in capitais.iterrows():
    uf = capital['uf'].lower()
    print('Capital:', capital['capital'])

    serie = serie_mensal_do_ponto(capital['lat'], capital['lon'])
    serie.to_csv(f'{BASE}/dados/capitais/{uf}.csv')

    print('   meses vazios:', serie['tmed'].isna().sum() + serie['chuva'].isna().sum())
```

> ⏳ Leva cerca de **1 minuto por capital**. Deixe rodando e confira no fim quais vieram com meses vazios.

### 4. Bônus: Xavier × INMET

Na fase 1, você digitou as normais do INMET de algumas capitais. Calcule agora a normal 1991–2020 do Xavier
para elas e compare mês a mês. A temperatura é parecida? E a chuva?

```python
# Normal 1991-2020 do Xavier para uma capital (média de cada mês)
serie = pd.read_csv(f'{BASE}/dados/capitais/df.csv', parse_dates=['data'], index_col='data')
periodo = serie.loc['1991':'2020']
normal_xavier = periodo.groupby(periodo.index.month).mean()
normal_xavier.round(1)
```

> 🧠 O INMET é uma **estação** (um ponto); o Xavier é um **pixel** de ~10 km, interpolado de várias estações.
> Pequenas diferenças são esperadas. Por quê?

---

## Se der erro

| Mensagem (última linha) | O que costuma ser |
|---|---|
| `ee.ee_exception.EEException: ... not registered to use Earth Engine` | o projeto não foi registrado no Earth Engine; volte ao passo 2 da semana 1 |
| `... Earth Engine API has not been used in project ...` | a API do Earth Engine não está ativada no projeto; o link da mensagem leva à página para ativar |
| `... project ... not found` ou `PERMISSION_DENIED` | o `PROJETO` está com o ID errado (confira: é o ID, não o nome) |
| `... User memory limit exceeded` ou `Computation timed out` | pedido grande demais; troque o `10` do `range` por `5` na função `serie_mensal_do_ponto` |
| `FileNotFoundError` | falta o atalho da pasta no "Meu Drive" (Missão 0, passo 1) |

## 📦 Entregável

- ✍️ A seção **Sua vez** do notebook de exemplo, feita para as capitais pedidas.
- O ID do seu projeto do GEE, anotado no diário.
- O resultado da conferência de Santa Helena (as duas diferenças).
- `dados/capitais_27.csv` e os 27 arquivos em `dados/capitais/`, sem meses vazios.
- Uma célula de texto listando as capitais em que você precisou mover a coordenada, e para onde.

## 🗣️ Para o próximo encontro, saiba responder

- O que é o Google Earth Engine e por que não baixamos a base inteira?
- O que fazem as funções `converter_para_unidades_fisicas`, `baixar_dias` e `serie_mensal_do_ponto`?
- Por que é importante que a sua série de Santa Helena seja igual à do arquivo do projeto?
- Por que algumas capitais do litoral vieram vazias?

## ✅ Checklist

- [ ] Criei e registrei o meu projeto no GEE (junto com o orientador)
- [ ] Autentiquei no Colab e vi as bandas da base do Xavier
- [ ] Extraí Santa Helena e conferi com o arquivo do projeto
- [ ] Montei a tabela das 27 capitais
- [ ] Extraí 3 capitais à mão e as outras com a célula pronta
- [ ] Respondi às perguntas sobre o bloco de extração
- [ ] Preenchi o diário de bordo
