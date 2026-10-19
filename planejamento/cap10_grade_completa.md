# Capítulo 10 — Grade Completa do Xavier (Fase B)

> **Objetivo do capítulo:** aplicar o mesmo método da Fase A a **todos os pixels** do Brasil: agregar para mensal no GEE, exportar para o Drive, calcular o clima de referência móvel e classificar cada pixel em cada ano.
> Notebook: `cap10_grade_completa.ipynb`
> ⚠️ Só comece este capítulo depois do ponto de controle do Capítulo 9.

---

## 10.1 O que muda da Fase A para a Fase B

| | Fase A (27 pontos) | Fase B (grade) |
|---|---|---|
| Unidade | ponto | pixel de 0,1° |
| Quantidade | 27 | dezenas de milhares |
| Saída do GEE | `.getInfo()` (pequeno) | **exportação** para o Drive (grande) |
| Estrutura no Python | `pandas` (tabela) | `xarray` (cubo tempo × lat × lon) |
| Método | clima móvel + classificação | **o mesmo** |

> 💡 É aqui que compensa ter escrito tudo em funções: a lógica não muda, só a forma dos dados.

---

## 10.2 Novas bibliotecas

```python
!pip install rioxarray

import ee
import numpy as np
import pandas as pd
import xarray as xr
import rioxarray

ee.Initialize(project='ee-seunome')
```

**xarray** trabalha com arrays de várias dimensões com nomes, como uma "tabela em 3D":

```
DataArray chuva
   dims: (time, y, x)
   time: 1961-01 ... 2020-12   (720 meses)
   y:    latitudes
   x:    longitudes
```

---

## 10.3 Agregando e exportando no GEE

Reaproveitamos a função `mensal_gee` do Capítulo 5. Cada exportação contém **uma variável e uma década**: 120 bandas, uma por mês.

```python
COLECOES = {
    'chuva': 'projects/sat-io/open-datasets/BR-DWGD/PR',
    'tmax':  'projects/sat-io/open-datasets/BR-DWGD/TMAX',
    'tmin':  'projects/sat-io/open-datasets/BR-DWGD/TMIN',
}
REDUCAO = {'chuva': 'soma', 'tmax': 'media', 'tmin': 'media'}

brasil = (ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
          .filter(ee.Filter.eq('country_na', 'Brazil')))
regiao = brasil.geometry().bounds()

# Usa exatamente a grade original do Xavier (sem reamostrar)
proj = ee.ImageCollection(COLECOES['chuva']).first().projection().getInfo()

tarefas = []
for var in COLECOES:
    for ini in range(1961, 2021, 10):
        fim = ini + 9
        img = (mensal_gee(COLECOES[var], ini, fim, REDUCAO[var])
               .toBands()
               .clip(brasil)
               .toFloat())
        tarefa = ee.batch.Export.image.toDrive(
            image=img,
            description=f'xavier_{var}_{ini}_{fim}',
            folder='xavier_mensal',
            region=regiao,
            crs=proj['crs'],
            crsTransform=proj['transform'],
            maxPixels=1e10,
        )
        tarefa.start()
        tarefas.append(tarefa)
        print('Enviada:', var, ini, fim)
```

Acompanhe as tarefas:

```python
for t in tarefas:
    print(t.status()['description'], t.status()['state'])
```

> ⏳ São 18 exportações (3 variáveis × 6 décadas). Elas rodam **no servidor**, mesmo com o Colab fechado. Acompanhe também na aba **Tasks** do Code Editor.
> ⚠️ O GEE cria a pasta `xavier_mensal` na **raiz** do Drive. Depois, mova-a para `mudanca_climatica_br/dados/`.

---

## 10.4 Abrindo os dados no Python

```python
PASTA = f'{BASE}/dados/xavier_mensal'


def abrir_variavel(var, ano_ini=1961, ano_fim=2020):
    """Junta as décadas de uma variável num único cubo (time, y, x)."""
    partes = []
    for ini in range(ano_ini, ano_fim + 1, 10):
        fim = ini + 9
        da = rioxarray.open_rasterio(f'{PASTA}/xavier_{var}_{ini}_{fim}.tif')
        datas = pd.date_range(f'{ini}-01-01', periods=da.sizes['band'], freq='MS')
        da = da.rename({'band': 'time'}).assign_coords(time=datas)
        partes.append(da)
    return xr.concat(partes, dim='time').rename(var)


chuva = abrir_variavel('chuva')
tmed = (abrir_variavel('tmax') + abrir_variavel('tmin')) / 2
print(chuva)
```

> ⚠️ Se o GEE dividir uma exportação em vários arquivos (`...-0000000000-0000000000.tif`), aumente `maxPixels` ou junte-os com `rioxarray.merge`.

**Validação obrigatória:** compare um pixel com a série do Capítulo 5.

```python
pixel = chuva.sel(x=-54.33, y=-24.86, method='nearest').to_series()
ref = pd.read_csv(f'{BASE}/dados/xavier_santa_helena_mensal_gee.csv',
                  index_col='data', parse_dates=True)['chuva']
print('Maior diferença (mm):', (pixel - ref).abs().max())
```

> ✅ A diferença deve ser praticamente zero. Não siga sem isso.

---

## 10.5 Clima de referência móvel na grade

Mesma lógica do Capítulo 3, agora em 3D:

```python
def clima_do_periodo_grade(da, ano_ini, ano_fim):
    """12 médias mensais (month, y, x) entre ano_ini e ano_fim."""
    sub = da.sel(time=slice(f'{ano_ini}-01-01', f'{ano_fim}-12-31'))
    return sub.groupby('time.month').mean('time')
```

---

## 10.6 Classificando cada pixel

Para a grade, a classificação precisa receber **arrays do numpy** (12 valores). Versão numpy da função do Capítulo 7 (meses 0 a 11):

```python
VERAO = [9, 10, 11, 0, 1, 2]     # out a mar (índices começam em 0)
INVERNO = [3, 4, 5, 6, 7, 8]     # abr a set


def koppen_np(t, p):
    """Köppen (versão didática) para arrays numpy de 12 valores."""
    if np.isnan(t).any() or np.isnan(p).any():
        return ''
    t_ano, p_ano = t.mean(), p.sum()
    frac_verao = p[VERAO].sum() / p_ano if p_ano > 0 else 0
    limiar = 20 * t_ano + (280 if frac_verao >= 0.7 else 140 if frac_verao >= 0.3 else 0)
    if p_ano < limiar:
        return 'BWh' if p_ano < limiar / 2 else 'BSh'
    if t.min() >= 18:
        if p.min() >= 60:
            return 'Af'
        if p.min() >= 100 - p_ano / 25:
            return 'Am'
        return 'As' if p[VERAO].min() < p[INVERNO].min() else 'Aw'
    terceira = 'a' if t.max() >= 22 else 'b'
    if p[INVERNO].min() < p[VERAO].max() / 10:
        segunda = 'w'
    elif p[VERAO].min() < 40 and p[VERAO].min() < p[INVERNO].max() / 3:
        segunda = 's'
    else:
        segunda = 'f'
    return 'C' + segunda + terceira
```

> ⚠️ Se a agrometeorologiapy aceitar arrays numpy, use a função da biblioteca no lugar de `koppen_np`.

Aplicando a todos os pixels com `xarray.apply_ufunc`:

```python
CLASSES = ['Af', 'Am', 'Aw', 'As', 'BWh', 'BSh',
           'Cfa', 'Cfb', 'Cwa', 'Cwb', 'Csa', 'Csb']
CODIGO = {c: i + 1 for i, c in enumerate(CLASSES)}   # 0 = sem dado


def classificar_grade(t_clim, p_clim, func=koppen_np):
    classes = xr.apply_ufunc(
        func, t_clim, p_clim,
        input_core_dims=[['month'], ['month']],
        vectorize=True,
        output_dtypes=[object],
    )
    return xr.apply_ufunc(lambda c: CODIGO.get(c, 0), classes,
                          vectorize=True, output_dtypes=[np.int8])
```

> 🧠 Guardamos **códigos inteiros** (1, 2, 3...) em vez de texto: ocupam menos espaço e podem ser salvos como GeoTIFF.

---

## 10.7 Rodando todos os anos

```python
import os

saida = f'{BASE}/resultados/grade'
os.makedirs(saida, exist_ok=True)

mapas = []
for ano in range(1990, 2021):
    ini, fim = janela_30_anos(ano)
    t_clim = clima_do_periodo_grade(tmed, ini, fim)
    p_clim = clima_do_periodo_grade(chuva, ini, fim)
    mapa = classificar_grade(t_clim, p_clim).expand_dims(ano=[ano])
    mapas.append(mapa)
    print(ano, 'ok')

koppen = xr.concat(mapas, dim='ano').rename('koppen')
koppen.to_netcdf(f'{saida}/koppen_1990_2020.nc')
pd.Series(CODIGO).to_csv(f'{saida}/legenda_koppen.csv', header=['codigo'])
```

> ⏳ Pode levar vários minutos. Teste antes com **um único ano**.
> 💡 Faça o mesmo para Thornthwaite, Camargo e Holdridge trocando a função em `classificar_grade`.

Mapas rápidos para conferir:

```python
import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 2, figsize=(14, 6))
koppen.sel(ano=1990).plot(ax=axs[0], cmap='tab20', vmin=0, vmax=20, add_colorbar=False)
koppen.sel(ano=2020).plot(ax=axs[1], cmap='tab20', vmin=0, vmax=20, add_colorbar=False)
axs[0].set_title('Köppen — clima de 1990 (1961–1990)')
axs[1].set_title('Köppen — clima de 2020 (1991–2020)')
plt.show()
```

**Validação:** compare visualmente o mapa de 1990 com o de Alvares et al. (2013) e confira se os pixels das 27 capitais repetem as classes do Capítulo 8.

---

## 10.8 Exercícios

1. Por que na Fase B usamos exportação e não `.getInfo()`?
2. Quantos pixels válidos (código ≠ 0) há no Brasil?
3. Confira 5 capitais: a classe do pixel bate com a do Capítulo 8?
4. Compare o mapa de 1990 com o de Alvares et al. (2013). Onde há diferenças? Por quê?
5. Repita a classificação da grade para outra classificação do Capítulo 9.

---

## ✅ Checklist do Capítulo 10

- [ ] Exportei as 18 imagens mensais do GEE para o Drive
- [ ] Abri e juntei as décadas no xarray
- [ ] Validei um pixel com a série do Capítulo 5
- [ ] Classifiquei um ano de teste e depois todos os anos
- [ ] Salvei `koppen_1990_2020.nc` e a legenda
- [ ] Conferi as capitais e comparei com Alvares et al. (2013)
- [ ] Respondi os exercícios

**Entregável 10:** notebook `cap10_grade_completa.ipynb` + `koppen_1990_2020.nc` (e das demais classificações) + mapas de 1990 e 2020.
