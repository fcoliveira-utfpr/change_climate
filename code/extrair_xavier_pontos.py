"""
Extrai do Google Earth Engine a série MENSAL do Xavier (BR-DWGD v3.2.4, 1961-2025)
para uma lista de pontos e salva um CSV por ponto.

Quem usa:
    - o orientador, para gerar os dados de exemplo (Santa Helena e Curitiba, em code/dados/);
    - a aluna, a partir da Missão 5 (notebook de exemplo 06), para extrair as capitais e outros lugares.

O que sai, para cada ponto da lista PONTOS:
    <pasta_saida>/<nome>_mensal.csv           -> colunas: data, tmed (°C), chuva (mm)
    <pasta_saida>/<nome>_normal_1991_2020.csv -> colunas: mes, tmed (°C), chuva (mm)

Como os dados são calculados:
    - tmed de cada dia = (Tmax + Tmin) / 2
    - tmed do mês      = média dos dias do mês
    - chuva do mês     = soma dos dias do mês
    - um mês com algum dia faltando fica vazio (NaN)

Como rodar no Colab:
    1. instale a biblioteca:  !pip install earthengine-api
    2. troque PROJETO pelo nome do seu projeto do Google Cloud
    3. edite a lista PONTOS e a PASTA_SAIDA
    4. rode o arquivo inteiro
"""

import ee
import pandas as pd


# =====================================================================
# 1. CONFIGURAÇÕES: a única parte que você precisa mudar
# =====================================================================

# Nome do seu projeto do Google Cloud registrado no Earth Engine
PROJETO = 'fcoliveira'

# Pasta onde os arquivos CSV serão salvos.
# No Colab, use a pasta do Drive: '/content/drive/MyDrive/mudanca_climatica_br/dados'
PASTA_SAIDA = '.'

# Pontos a extrair. Cada ponto tem um nome (sem acento e sem espaço),
# a latitude e a longitude, em graus (negativas no Brasil).
PONTOS = [
    {'nome': 'santa_helena', 'lat': -24.86, 'lon': -54.33},
    {'nome': 'curitiba', 'lat': -25.43, 'lon': -49.27},
]

# Período da série
PRIMEIRO_ANO = 1961
ULTIMO_ANO = 2025


# =====================================================================
# 2. CONEXÃO COM O EARTH ENGINE
# =====================================================================

# Abre a janela de login do Google (só na primeira vez) e conecta ao projeto
ee.Authenticate()
ee.Initialize(project=PROJETO)

# Endereço da base do Xavier v3.2.4 no Earth Engine (dados diários, 0,1°)
ASSET_XAVIER = 'projects/ee-alexandrexavier/assets/BR-DWGD'


# =====================================================================
# 3. FUNÇÕES
# =====================================================================

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

    # Agrega em meses ('MS' = início do mês).
    # min_count = número de dias do mês: se faltar algum dia, o mês fica vazio.
    dias_no_mes = diaria['tmed'].resample('MS').size()
    dias_com_dado_t = diaria['tmed'].resample('MS').count()
    dias_com_dado_p = diaria['chuva'].resample('MS').count()

    mensal = pd.DataFrame()
    mensal['tmed'] = diaria['tmed'].resample('MS').mean()
    mensal['chuva'] = diaria['chuva'].resample('MS').sum()

    # Apaga os meses incompletos
    mensal.loc[dias_com_dado_t < dias_no_mes, 'tmed'] = float('nan')
    mensal.loc[dias_com_dado_p < dias_no_mes, 'chuva'] = float('nan')

    mensal.index.name = 'data'
    return mensal.round(2)


def normal_1991_2020(mensal):
    """Normal 1991-2020: média de cada mês do ano (12 linhas)."""
    periodo = mensal.loc['1991':'2020']
    normal = periodo.groupby(periodo.index.month).mean()
    normal.index.name = 'mes'
    return normal.round(1)


# =====================================================================
# 4. EXECUÇÃO: um ponto de cada vez
# =====================================================================

for ponto in PONTOS:
    print('Ponto:', ponto['nome'])

    mensal = serie_mensal_do_ponto(ponto['lat'], ponto['lon'])
    arquivo_mensal = f"{PASTA_SAIDA}/{ponto['nome']}_mensal.csv"
    mensal.to_csv(arquivo_mensal)

    normal = normal_1991_2020(mensal)
    arquivo_normal = f"{PASTA_SAIDA}/{ponto['nome']}_normal_1991_2020.csv"
    normal.to_csv(arquivo_normal)

    # Conferência rápida
    meses_vazios = mensal['tmed'].isna().sum() + mensal['chuva'].isna().sum()
    print('   meses na série:', len(mensal), '| valores faltando:', meses_vazios)
    print('   salvo em', arquivo_mensal, 'e', arquivo_normal)

print('Pronto!')
