# Capítulo 6 — Os 27 Pontos a partir dos Centroides das Capitais

> **Objetivo do capítulo:** montar a tabela dos 27 pontos (26 capitais + Brasília) a partir do asset de centroides dos municípios e extrair a série mensal do Xavier para todos eles.
> Notebook: `cap06_27_pontos.ipynb`

---

## 6.1 Por que um ponto por estado?

- Cobre todas as regiões do Brasil com pouco processamento.
- Permite comparar climas muito diferentes (Amazônia, Semiárido, Sul).
- Usamos o **centroide do município da capital** porque o asset disponível é de **municípios**.

> ⚠️ **Limitação:** um ponto não representa um estado inteiro. Em estados grandes (AM, PA, MT, MG, BA) o clima da capital pode ser bem diferente do interior. Os resultados da Fase A falam sobre **as capitais**, não sobre os estados.

---

## 6.2 Conhecendo o asset

```python
import ee
import pandas as pd

ee.Initialize(project='ee-seunome')

ASSET = '_______________'   # o orientador vai informar
municipios = ee.FeatureCollection(ASSET)

print('Número de municípios:', municipios.size().getInfo())
print('Campos disponíveis:', municipios.first().propertyNames().getInfo())
print(municipios.first().getInfo())
```

> ✍️ Anote os nomes dos campos de **nome do município**, **UF** e **código IBGE**. Eles serão usados abaixo nas variáveis `CAMPO_NOME` e `CAMPO_UF`.

---

## 6.3 Filtrando as 27 capitais

```python
CAMPO_NOME = 'NOME_DO_CAMPO'   # ex.: nome do município
CAMPO_UF = 'CAMPO_DA_UF'       # ex.: sigla da UF

CAPITAIS = [
    ('AC', 'Rio Branco'), ('AL', 'Maceió'), ('AP', 'Macapá'),
    ('AM', 'Manaus'), ('BA', 'Salvador'), ('CE', 'Fortaleza'),
    ('DF', 'Brasília'), ('ES', 'Vitória'), ('GO', 'Goiânia'),
    ('MA', 'São Luís'), ('MT', 'Cuiabá'), ('MS', 'Campo Grande'),
    ('MG', 'Belo Horizonte'), ('PA', 'Belém'), ('PB', 'João Pessoa'),
    ('PR', 'Curitiba'), ('PE', 'Recife'), ('PI', 'Teresina'),
    ('RJ', 'Rio de Janeiro'), ('RN', 'Natal'), ('RS', 'Porto Alegre'),
    ('RO', 'Porto Velho'), ('RR', 'Boa Vista'), ('SC', 'Florianópolis'),
    ('SP', 'São Paulo'), ('SE', 'Aracaju'), ('TO', 'Palmas'),
]

linhas = []
for uf, nome in CAPITAIS:
    f = municipios.filter(ee.Filter.And(
        ee.Filter.eq(CAMPO_UF, uf),
        ee.Filter.eq(CAMPO_NOME, nome)
    )).first()
    coords = f.geometry().centroid().coordinates().getInfo()   # [lon, lat]
    linhas.append({'uf': uf, 'municipio': nome,
                   'lat': coords[1], 'lon': coords[0]})
    print(uf, nome, coords)

pontos = pd.DataFrame(linhas)
pontos
```

> ⚠️ Se algum nome não for encontrado, confira acentos e maiúsculas no asset (ex.: "Sao Luis" × "São Luís").
> 💡 Se o asset já for de pontos, `.centroid()` devolve o próprio ponto, então o código funciona nos dois casos.

**Confira:** a tabela deve ter **27 linhas**, sem coordenadas repetidas.

```python
print(len(pontos))
pontos.to_csv(f'{BASE}/dados/pontos_27_capitais.csv', index=False)
```

---

## 6.4 Mapa dos 27 pontos

```python
import geemap

Map = geemap.Map(center=[-15, -55], zoom=4)
for _, p in pontos.iterrows():
    Map.addLayer(ee.Geometry.Point([p['lon'], p['lat']]),
                 {'color': 'red'}, p['uf'])
Map
```

> 🧠 Olhe o mapa e pergunte-se: quais regiões ficam sem nenhum ponto?

---

## 6.5 Extraindo a série dos 27 pontos

Agora reaproveitamos a função `extrair_serie` do Capítulo 5 (copie para este notebook as funções `mensal_gee`, `ler_no_ponto` e `extrair_serie`).

```python
import os

pasta = f'{BASE}/dados/series_27'
os.makedirs(pasta, exist_ok=True)

for _, p in pontos.iterrows():
    arquivo = f"{pasta}/{p['uf']}.csv"
    if os.path.exists(arquivo):          # já baixado? pula
        print(p['uf'], 'já existe')
        continue
    try:
        df = extrair_serie(p['lat'], p['lon'])
        df.to_csv(arquivo)
        print(p['uf'], 'ok', len(df), 'meses')
    except Exception as erro:
        print(p['uf'], 'ERRO:', erro)
```

Entendendo:
- **Um arquivo por ponto:** se a sessão cair, nada se perde.
- `if os.path.exists(...)`: ao rodar de novo, só baixa o que falta.
- `try/except`: um erro num ponto não interrompe os outros.

---

## 6.6 Conferindo os dados

```python
resumo = []
for uf in pontos['uf']:
    df = pd.read_csv(f'{pasta}/{uf}.csv', index_col='data', parse_dates=True)
    resumo.append({
        'uf': uf,
        'meses': len(df),
        'falhas': int(df.isna().sum().sum()),
        'chuva_anual_media': df['chuva'].resample('YS').sum().mean(),
        'tmed_media': df['tmed'].mean(),
    })

resumo = pd.DataFrame(resumo).round(1)
resumo
```

> ✅ Todos devem ter o mesmo número de meses e nenhuma falha. Confira se os valores fazem sentido: Manaus quente e chuvosa, Porto Alegre mais fria, capitais do Nordeste com chuva menor.

---

## 6.7 Exercícios

1. Quais estados você acha que ficam pior representados pela capital? Justifique.
2. Ordene a tabela `resumo` pela temperatura média. Qual a capital mais quente e a mais fria?
3. Faça um gráfico de barras da chuva anual média das 27 capitais.
4. Faça os climogramas de 1991–2020 de três capitais de regiões diferentes e compare.
5. Por que salvamos um arquivo por ponto, e não um arquivo único no final?

---

## ✅ Checklist do Capítulo 6

- [ ] Explorei o asset e anotei os nomes dos campos
- [ ] Montei a tabela dos 27 pontos e salvei `pontos_27_capitais.csv`
- [ ] Fiz o mapa dos pontos
- [ ] Extraí e salvei as 27 séries mensais
- [ ] Conferi falhas e valores na tabela `resumo`
- [ ] Respondi os exercícios

**Entregável 6:** notebook `cap06_27_pontos.ipynb` + `pontos_27_capitais.csv` + pasta `series_27/` com 27 arquivos + mapa dos pontos.
