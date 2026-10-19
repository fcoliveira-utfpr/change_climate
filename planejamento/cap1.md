# Capítulo 1 — Apresentação do Projeto e Conceitos Fundamentais

> **Objetivo do capítulo:** entender O QUE vamos fazer e POR QUÊ, antes de escrever qualquer linha de código.

---

## 1.1 A pergunta da pesquisa

> **O clima do Brasil está mudando? Onde, quanto e desde quando?**

Para responder, vamos:
1. calcular o "clima" de cada ano usando os 30 anos anteriores;
2. classificar esse clima (principalmente por Köppen);
3. observar se a classe de um local **muda ao longo dos anos**.

Se um local era "Cfa" e passa a ser "Aw", o clima dele mudou de categoria: uma evidência concreta e fácil de comunicar.

---

## 1.2 Tempo × Clima

- **Tempo (meteorológico):** estado da atmosfera num momento. Ex.: "hoje chove e faz 18 °C".
- **Clima:** comportamento **médio** da atmosfera ao longo de muitos anos. Ex.: "Santa Helena tem verões quentes e chuva bem distribuída".

> Um ano muito seco é **variabilidade**. Vários anos alterando a média é **mudança climática**.

---

## 1.3 Normal Climatológica

A Organização Meteorológica Mundial (OMM) define a **Normal Climatológica** como a média de uma variável em **30 anos**, tempo suficiente para diluir anos atípicos. As normais oficiais usam períodos **fixos** (ex.: 1961–1990, 1991–2020).

**Problema:** períodos fixos dão poucos "retratos" do clima, um a cada 30 anos.

---

## 1.4 Nossa abordagem: Clima de Referência Móvel

Cada **ano** recebe um clima calculado com os **30 anos que terminam nele**:

| Ano | Período usado |
|---|---|
| 1990 | 1961–1990 |
| 1991 | 1962–1991 |
| 2000 | 1971–2000 |

A cada ano a janela avança: entra o ano novo, sai o mais antigo.

**Consequências:**
- O primeiro ano classificável é o 30º da série (dados desde 1961 → primeiro ano 1990).
- Teremos **uma classificação por ano**, mostrando **quando** a mudança ocorre.
- Janelas vizinhas compartilham 29 anos, então mudam devagar e revelam **tendências**, não oscilações.

> Não é a normal oficial da OMM; por isso usamos o termo **clima de referência móvel**.

---

## 1.5 Classificação climática

Agrupa locais de clima parecido em **classes**, com regras sobre temperatura, chuva e, às vezes, evapotranspiração.

**Köppen (principal):** usa temperatura e precipitação mensais.
- 1ª letra, grupo: A (tropical), B (seco), C (temperado). D e E não ocorrem no Brasil.
- 2ª letra, chuva: f (o ano todo), w (inverno seco), s (verão seco), m (monção).
- 3ª letra, verão: a (quente), b (ameno).
- Ex.: **Cfa** = temperado, sem estação seca, verão quente (oeste do Paraná).

**Thornthwaite:** baseada no **balanço hídrico** (chuva × evapotranspiração potencial); indica excesso ou deficiência de água.

**Camargo:** classificação brasileira, também apoiada no balanço hídrico e voltada à agricultura.

**Holdridge (Zonas de Vida):** usa **biotemperatura** e **precipitação anual** para definir zonas ligadas à vegetação natural.

> Todas estão implementadas na **agrometeorologiapy**, usada nos próximos capítulos.

---

## 1.6 Os dados: base do Xavier

Dados meteorológicos **diários** em **grade** para todo o Brasil, resolução de **0,1°** (≈10 km), gerados a partir de milhares de estações e pluviômetros. Variáveis principais: precipitação, temperatura máxima e mínima (há também evapotranspiração, radiação, umidade e vento).

Está no **Google Earth Engine (GEE)**, que processa dados geográficos na nuvem sem precisar baixá-los. Detalhes no Capítulo 4.
