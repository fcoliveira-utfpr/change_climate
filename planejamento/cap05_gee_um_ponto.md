# Capítulo 5 — Extraindo a Série de um Ponto no GEE

> **Objetivo do capítulo:** entender, linha por linha, como os dados saem do GEE e chegam ao pandas, e construir a função de extração que será usada no resto do projeto.
> Notebook: `cap05_gee_um_ponto.ipynb`

---

## 5.1 O caminho do dado

```
GEE (servidor)                                Colab (seu notebook)
ImageCollection diária
   → filtrar período
   → selecionar banda
   → (opcional) agregar para mensal
   → ler o valor no ponto  ──── .getInfo() ───→ lista Python → DataFrame pandas
```

Tudo antes de `.getInfo()` acontece **no servidor do Google**. Só o resultado final viaja para o Colab. Quanto menor esse resultado, mais rápido e seguro.

---

## 5.2 Os blocos básicos do GEE

| Comando | O que faz |
|---|---|
| `ee.ImageCollection(id)` | abre uma coleção |
| `.filterDate(ini, fim)` | mantém só as imagens do período (o `fim` **não** é incluído) |
| `.select([0])` ou `.select('nome')` | escolhe a banda |
| `.sum()` / `.mean()` | junta várias imagens em uma só |
| `.map(funcao)` | aplica uma função a cada imagem |
| `ee.Geometry.Point([lon, lat])` | cria um ponto |
| `.getRegion(ponto, escala)` | lê o valor de **todas as imagens** no ponto |
| `.getInfo()` | traz o resultado para o Colab |

> ⚠️ `filterDate('2000-01-01', '2001-01-01')` pega **todo o ano 2000**, porque a data final é excluída.

---

## 5.3 Entendendo a "receita pronta" do Capítulo 3

**Passo 1 — Abrir, filtrar e selecionar:**

```python
import ee
import pandas as pd

ee.Initialize(project='ee-seunome')

ponto = ee.Geometry.Point([-54.33, -24.86])   # Santa Helena-PR [lon, lat]

col = (ee.ImageCollection('projects/sat-io/open-datasets/BR-DWGD/PR')
       .filterDate('2000-01-01', '2001-01-01')
       .select([0]))

print(col.size().getInfo())   # deve ser 366 (2000 foi bissexto)
```

**Passo 2 — Ler os valores no ponto:**

```python
linhas = col.getRegion(ponto, 10000).getInfo()
print(linhas[0])    # cabeçalho
print(linhas[1])    # primeiro dia
```

O resultado é uma lista de listas:
```
['id', 'longitude', 'latitude', 'time', 'b1']    ← cabeçalho (o nome da banda pode variar)
['...', -54.33, -24.86, 946684800000, 3.2]        ← um dia
```

- `time` está em **milissegundos desde 1970** (padrão do GEE).
- A última coluna é o valor da variável.
- A escala `10000` (10 km) corresponde à resolução da grade (0,1°).

**Passo 3 — Converter para pandas:**

```python
tab = pd.DataFrame(linhas[1:], columns=linhas[0])
serie = pd.Series(tab.iloc[:, 4].astype(float).values,
                  index=pd.to_datetime(tab['time'], unit='ms'))
serie.head()
```

- `linhas[1:]` → todas as linhas menos o cabeçalho
- `tab.iloc[:, 4]` → a 5ª coluna (o valor)
- `unit='ms'` → converte milissegundos em data

**Passo 4 — Por que extrair década a década?**

O GEE limita o tamanho das respostas e o tempo de processamento. Pedir 60 anos de dados diários de uma vez pode gerar erro de memória ou de tempo. Dividindo em blocos de 10 anos, cada pedido fica pequeno e depois juntamos tudo com `pd.concat`.

---

## 5.4 Erros comuns e como resolver

| Erro | Causa provável | Solução |
|---|---|---|
| `EEException: Collection.getRegion: Too many values` | período longo demais num pedido só | dividir em blocos menores |
| `Computation timed out` | servidor demorou demais | blocos menores ou agregação no GEE (seção 5.5) |
| Valores todos `None` | ponto fora do Brasil ou lat/lon invertidos | conferir a ordem `[lon, lat]` |
| `Please authorize access` | sessão nova do Colab | rodar `ee.Authenticate()` de novo |
| Série com datas faltando | `filterDate` com data final errada | lembrar que a data final é excluída |

---

## 5.5 Agregando para mensal dentro do GEE

O método só precisa de dados **mensais**. Se agregarmos no servidor, o Colab recebe 12 valores por ano em vez de 365: cerca de **30 vezes menos dados**. Isso será essencial com 27 pontos e com a grade completa.

```python
def mensal_gee(colecao_id, ano_ini, ano_fim, reducao):
    """
    Cria, no GEE, uma coleção MENSAL a partir da coleção diária.
    reducao = 'soma' (chuva) ou 'media' (temperatura).
    """
    col = ee.ImageCollection(colecao_id).select([0])
    inicio = ee.Date.fromYMD(ano_ini, 1, 1)
    n_meses = (ano_fim - ano_ini + 1) * 12

    def um_mes(i):
        d = inicio.advance(i, 'month')
        mes = col.filterDate(d, d.advance(1, 'month'))
        img = mes.sum() if reducao == 'soma' else mes.mean()
        return img.rename('valor').set('system:time_start', d.millis())

    return ee.ImageCollection(ee.List.sequence(0, n_meses - 1).map(um_mes))
```

Entendendo:
- `ee.List.sequence(0, n_meses - 1)` → lista 0, 1, 2, ... (um número por mês)
- `.map(um_mes)` → para cada número, cria a imagem daquele mês
- `.rename('valor')` → padroniza o nome da banda
- `.set('system:time_start', ...)` → grava a data do mês na imagem

> 🧠 O `if reducao == 'soma'` é Python comum: é decidido **antes** de enviar ao servidor. Chuva = soma; temperatura = média (Capítulo 3).

---

## 5.6 A função final de extração

Esta função será usada em **todos** os próximos capítulos.

```python
COLECOES = {
    'chuva': 'projects/sat-io/open-datasets/BR-DWGD/PR',
    'tmax':  'projects/sat-io/open-datasets/BR-DWGD/TMAX',
    'tmin':  'projects/sat-io/open-datasets/BR-DWGD/TMIN',
}


def ler_no_ponto(col_mensal, ponto):
    """Lê uma coleção mensal num ponto e devolve uma Series do pandas."""
    linhas = col_mensal.getRegion(ponto, 10000).getInfo()
    tab = pd.DataFrame(linhas[1:], columns=linhas[0])
    serie = pd.Series(tab['valor'].astype(float).values,
                      index=pd.to_datetime(tab['time'], unit='ms'))
    return serie.sort_index()


def extrair_serie(lat, lon, ano_ini=1961, ano_fim=2020):
    """
    Série MENSAL do Xavier num ponto: chuva (mm/mês) e tmed (°C).
    """
    ponto = ee.Geometry.Point([lon, lat])
    chuva = ler_no_ponto(mensal_gee(COLECOES['chuva'], ano_ini, ano_fim, 'soma'), ponto)
    tmax = ler_no_ponto(mensal_gee(COLECOES['tmax'], ano_ini, ano_fim, 'media'), ponto)
    tmin = ler_no_ponto(mensal_gee(COLECOES['tmin'], ano_ini, ano_fim, 'media'), ponto)

    df = pd.DataFrame({'chuva': chuva, 'tmax': tmax, 'tmin': tmin})
    df['tmed'] = (df['tmax'] + df['tmin']) / 2
    df.index.name = 'data'
    return df


mensal = extrair_serie(-24.86, -54.33)
mensal.head()
```

> 💡 Repare: a função recebe só **latitude e longitude**. No Capítulo 6, basta chamá-la num `for` para os 27 pontos.
> ⚠️ A média mensal de `tmed` calculada como (Tmax mensal + Tmin mensal) / 2 é igual à média dos `tmed` diários, desde que não haja falhas.

Salve:

```python
mensal.to_csv(f'{BASE}/dados/xavier_santa_helena_mensal_gee.csv')
```

---

## 5.7 Validando: o resultado bate com o Capítulo 3?

Nunca confie num código novo sem conferir. Compare com a série mensal calculada no pandas no Capítulo 3:

```python
antigo = pd.read_csv(f'{BASE}/dados/xavier_santa_helena_mensal.csv',
                     index_col=0, parse_dates=True)

dif_chuva = (mensal['chuva'] - antigo['chuva']).abs().max()
dif_tmed = (mensal['tmed'] - antigo['tmed']).abs().max()

print(f'Maior diferença de chuva: {dif_chuva:.3f} mm')
print(f'Maior diferença de tmed:  {dif_tmed:.3f} °C')
```

> ✅ As diferenças devem ser praticamente zero. Se não forem, confira datas, agregação (soma × média) e coordenadas antes de seguir.

---

## 5.8 Exercícios

1. Explique, com suas palavras, o que acontece no servidor e o que acontece no Colab na função `extrair_serie`.
2. Meça o tempo da extração diária (Cap. 3) e da mensal (Cap. 5) com `%%time` no início da célula. Qual foi mais rápida?
3. Extraia a série de Curitiba (lat -25.43, lon -49.27) e faça o climograma de 1991–2020.
4. Inverta propositalmente lat e lon e observe o erro ou resultado. Explique o que aconteceu.
5. Modifique `mensal_gee` para também extrair a ETo (coleção `ETO`, com soma mensal).

---

## ✅ Checklist do Capítulo 5

- [ ] Entendi cada passo da extração diária (seção 5.3)
- [ ] Criei a função `mensal_gee` e entendi a agregação no servidor
- [ ] Criei as funções `ler_no_ponto` e `extrair_serie`
- [ ] Salvei a série mensal de Santa Helena no Drive
- [ ] Validei o resultado com a série do Capítulo 3
- [ ] Respondi os exercícios

**Entregável 5:** notebook `cap05_gee_um_ponto.ipynb` + `xavier_santa_helena_mensal_gee.csv` + resultado da validação (seção 5.7).
