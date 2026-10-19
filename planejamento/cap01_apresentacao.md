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

---

## 1.7 Estratégia do projeto

O Brasil inteiro tem dezenas de milhares de pixels. Por isso, vamos em duas fases:

**Fase A — Aprender com 27 pontos**
- Um ponto por estado: o **centroide do município da capital** (26 capitais + Brasília).
- Primeiro fazemos o método completo em **um único ponto**; depois repetimos para os 27.
- Volume de dados pequeno: rápido de processar e fácil de conferir.
- Objetivo: dominar o método, o código e a interpretação.

**Fase B — Grade completa**
- O mesmo método aplicado a **cada pixel** da base do Xavier.
- Processamento pesado, feito em grande parte dentro do GEE.
- Só começa depois que a Fase A estiver validada com o orientador.

> 💡 Se o código da Fase A for escrito em **funções**, a Fase B quase não exige retrabalho: muda a entrada (pontos → pixels), e o método continua o mesmo.

---

## 1.8 Fluxo geral do método

1. **Dados diários** (Xavier, GEE)
2. **Agregação mensal**: precipitação = soma; temperatura = média
3. **Clima de referência móvel**: para cada ano, as 12 médias mensais dos 30 anos anteriores
4. **Classificação climática** de cada ano (Köppen e outras)
5. **Análise da mudança**: em que ano a classe mudou? Para qual classe?
6. **Estatística de tendência** na série anual (Mann-Kendall e Sen)
7. **Mapas e interpretação**

---

## 1.9 Glossário

- **Série temporal:** sequência de valores ordenados no tempo.
- **Agregação:** transformar dados diários em mensais ou anuais.
- **Janela móvel:** período de tamanho fixo que avança no tempo.
- **Pixel:** menor quadrado da grade; cada um tem seu próprio valor.
- **Centroide:** ponto central de uma área (aqui, de um município).
- **Tendência:** aumento ou diminuição sistemática ao longo do tempo.
- **GEE:** Google Earth Engine, plataforma de processamento geoespacial na nuvem.
- **Colab:** Google Colaboratory, ambiente para rodar Python no navegador.

---

## 1.10 Leituras recomendadas

- ALVARES, C. A. et al. Köppen's climate classification map for Brazil. *Meteorologische Zeitschrift*, v. 22, n. 6, p. 711–728, 2013.
- XAVIER, A. C. et al. New improved Brazilian daily weather gridded data (1961–2020). *International Journal of Climatology*, 2022.
- THORNTHWAITE, C. W. An approach toward a rational classification of climate. *Geographical Review*, v. 38, n. 1, p. 55–94, 1948.
- HOLDRIDGE, L. R. Determination of world plant formations from simple climatic data. *Science*, v. 105, n. 2727, p. 367–368, 1947.

---

## 1.11 Exercícios

1. Explique com suas palavras a diferença entre tempo e clima.
2. Qual seria o período usado para calcular o clima do ano de 2015?
3. Se a base começa em 1961, por que não é possível classificar o clima de 1975?
4. Procure a classificação de Köppen da sua cidade natal em Alvares et al. (2013) e explique o significado de cada letra.
5. Por que começamos com 27 pontos e não com o Brasil inteiro?

---

## ✅ Checklist do Capítulo 1

- [ ] Li o capítulo inteiro
- [ ] Li o artigo de Alvares et al. (2013), pelo menos a introdução e a metodologia
- [ ] Respondi os exercícios
- [ ] Discuti as respostas com o orientador

**Entregável 1:** documento curto (1 a 2 páginas) com as respostas dos exercícios.
