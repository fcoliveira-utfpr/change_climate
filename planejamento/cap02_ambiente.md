# Capítulo 2 — Ambiente de Trabalho: Colab, Drive e Google Earth Engine

> **Objetivo do capítulo:** deixar todas as ferramentas funcionando e entender o papel de cada uma.

---

## 2.1 As três ferramentas e o papel de cada uma

| Ferramenta | Para que serve no projeto |
|---|---|
| **Google Colab** | Onde escrevemos e rodamos o código Python, no navegador |
| **Google Drive** | Onde guardamos notebooks, tabelas, figuras e arquivos exportados |
| **Google Earth Engine** | Onde estão os dados do Xavier e onde fazemos o processamento pesado |

> Pense assim: o **GEE** é o depósito e a fábrica de dados, o **Colab** é a bancada de trabalho e o **Drive** é o arquivo onde guardamos os resultados.

---

## 2.2 Organizando o Google Drive

Crie esta estrutura de pastas:

    mudanca_climatica_br/
    ├── notebooks/     → arquivos .ipynb (um por capítulo)
    ├── dados/         → CSVs e arquivos baixados
    ├── resultados/    → tabelas finais
    ├── figuras/       → gráficos e mapas
    └── tutorial/      → os capítulos deste tutorial

**Regra de nomes:** sem acentos, sem espaços, com número do capítulo.
Ex.: `cap05_gee_um_ponto.ipynb`, `serie_santa_helena.csv`.

---

## 2.3 Google Colab

O Colab é um **notebook**: um documento com dois tipos de célula:
- **Código:** roda Python (botão ▶ ou `Shift + Enter`).
- **Texto:** explicações em Markdown (títulos, listas, anotações).

**Boas práticas:**
- Comece todo notebook com uma célula de texto: título, objetivo e data.
- Explique em texto o que cada bloco de código faz.
- Rode as células **de cima para baixo**. Se der erro estranho: `Ambiente de execução → Reiniciar sessão` e rode tudo de novo.
- O Colab **apaga** os arquivos da sessão quando desconecta. Salve sempre no Drive.

### Conectando o Colab ao Drive

```python
from google.colab import drive
drive.mount('/content/drive')

# Caminho base do projeto
BASE = '/content/drive/MyDrive/mudanca_climatica_br'
```

Teste:

```python
import os
print(os.listdir(BASE))   # deve listar as pastas criadas em 2.2
```

---

## 2.4 Google Earth Engine

### Cadastro
1. Acesse https://code.earthengine.google.com/register
2. Escolha **uso não comercial / acadêmico**.
3. Crie um **projeto Google Cloud** (ex.: `ee-seunome`). Anote o **ID do projeto**.
4. Aguarde a aprovação (às vezes é imediata).

### O Code Editor (navegador)
Em https://code.earthengine.google.com é possível testar visualmente, em JavaScript. Usaremos principalmente o **Python no Colab**, mas o Code Editor ajuda a **visualizar** dados no mapa.

### Conectando o GEE ao Colab

```python
import ee

ee.Authenticate()                      # abre uma janela para autorizar sua conta
ee.Initialize(project='ee-seunome')    # troque pelo ID do SEU projeto
```

Teste se funcionou:

```python
ponto = ee.Geometry.Point([-54.33, -24.86])   # Santa Helena-PR (lon, lat)
print(ponto.getInfo())
```

> ⚠️ **Atenção à ordem:** no GEE as coordenadas são **[longitude, latitude]**. Inverter é o erro mais comum.

### Conceito-chave: o GEE é "preguiçoso"
Os comandos do GEE **não rodam na hora**: eles montam uma "receita" no servidor. Os cálculos só acontecem quando pedimos o resultado, por exemplo com `.getInfo()` ou uma exportação. Por isso:
- `.getInfo()` deve ser usado só para resultados **pequenos**.
- Resultados grandes devem ser **exportados** para o Drive (Capítulo 10).

---

## 2.5 Instalando bibliotecas

Algumas bibliotecas já vêm no Colab; outras precisam ser instaladas **em cada sessão**:

```python
!pip install geemap pymannkendall
!pip install git+https://github.com/fcoliveira-utfpr/agrometeorologiapy
```

| Biblioteca | Uso |
|---|---|
| `earthengine-api` (`ee`) | acesso ao GEE (já vem no Colab) |
| `geemap` | mapas interativos com dados do GEE |
| `pandas`, `numpy` | tabelas e cálculos |
| `matplotlib` | gráficos |
| `pymannkendall` | testes de tendência (Capítulo 8) |
| `agrometeorologiapy` | classificações climáticas |

---

## 2.6 Primeiro mapa

```python
import geemap

Map = geemap.Map(center=[-24.86, -54.33], zoom=8)   # aqui é [lat, lon]!
Map.addLayer(ponto, {'color': 'red'}, 'Santa Helena')
Map
```

> Repare: o `geemap.Map` usa **[lat, lon]**, ao contrário do `ee.Geometry.Point`. Sempre confira.

---

## 2.7 Exercícios

1. Crie a estrutura de pastas da seção 2.2.
2. Crie o notebook `cap02_ambiente.ipynb` com: célula de título, montagem do Drive, autenticação do GEE e o mapa da seção 2.6.
3. Adicione ao mapa um ponto na sua cidade natal, com outra cor.
4. Explique, numa célula de texto, por que não devemos usar `.getInfo()` para dados grandes.

---

## ✅ Checklist do Capítulo 2

- [ ] Estrutura de pastas criada no Drive
- [ ] Cadastro no GEE aprovado e ID do projeto anotado
- [ ] Colab conectado ao Drive
- [ ] Colab conectado ao GEE
- [ ] Bibliotecas instaladas sem erro
- [ ] Mapa com os dois pontos funcionando
- [ ] Exercícios respondidos

**Entregável 2:** notebook `cap02_ambiente.ipynb` rodando do início ao fim sem erros + print do mapa.
