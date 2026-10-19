# Capítulo 11 — Análise Espacial e Redação dos Resultados

> **Objetivo do capítulo:** transformar os mapas do Capítulo 10 em resultados: quanto de área mudou, de qual classe para qual, onde há tendência significativa, e como escrever e divulgar o trabalho.
> Notebook: `cap11_analise_espacial.ipynb`

---

## 11.1 Perguntas que este capítulo responde

1. Quanta área do Brasil pertence a cada classe, ano a ano?
2. Entre o clima de 1990 e o de 2020, quais classes se transformaram em quais? Quantos km²?
3. Onde estão os pixels que mudaram?
4. Onde a temperatura e a chuva têm tendência significativa?

---

## 11.2 Carregando os resultados

```python
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

saida = f'{BASE}/resultados/grade'
koppen = xr.open_dataarray(f'{saida}/koppen_1990_2020.nc')
legenda = pd.read_csv(f'{saida}/legenda_koppen.csv', index_col=0)['codigo']
NOME = {v: k for k, v in legenda.items()}     # código → classe
```

---

## 11.3 Área de cada pixel

Em graus, os pixels **não têm a mesma área**: ficam menores à medida que se afastam do Equador.

Área aproximada de um pixel de 0,1° (km²):

> A ≈ (0,1 × 111,32)² × cos(latitude)

```python
area_pixel = (0.1 * 111.32) ** 2 * np.cos(np.deg2rad(koppen['y']))
area_pixel = area_pixel.broadcast_like(koppen.isel(ano=0))
```

> 🧠 Contar pixels em vez de somar área superestima as classes do Sul em relação às do Norte.

---

## 11.4 Área por classe ao longo do tempo

```python
linhas = []
for ano in koppen['ano'].values:
    mapa = koppen.sel(ano=ano)
    for cod in np.unique(mapa.values):
        if cod == 0:
            continue
        area = float(area_pixel.where(mapa == cod).sum())
        linhas.append({'ano': ano, 'classe': NOME[cod], 'area_km2': area})

areas = pd.DataFrame(linhas).pivot(index='ano', columns='classe', values='area_km2').fillna(0)
areas_pct = areas.div(areas.sum(axis=1), axis=0) * 100

areas.round(0).to_csv(f'{BASE}/resultados/area_por_classe_km2.csv')
areas_pct.round(2)
```

```python
fig, ax = plt.subplots(figsize=(10, 5))
areas_pct.plot(ax=ax, marker='o')
ax.set_ylabel('% da área do Brasil')
ax.set_xlabel('Ano (fim da janela de 30 anos)')
ax.set_title('Área por classe de Köppen — clima de referência móvel')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
ax.grid(alpha=0.3)
plt.show()
fig.savefig(f'{BASE}/figuras/area_por_classe.png', dpi=300, bbox_inches='tight')
```

---

## 11.5 Matriz de transição (1990 → 2020)

Mostra, em km², quanto de cada classe em 1990 virou cada classe em 2020. A **diagonal** é o que não mudou.

```python
c90 = koppen.sel(ano=1990).values.ravel()
c20 = koppen.sel(ano=2020).values.ravel()
a = area_pixel.values.ravel()

validos = (c90 > 0) & (c20 > 0)
trans = pd.DataFrame({'de': [NOME[c] for c in c90[validos]],
                      'para': [NOME[c] for c in c20[validos]],
                      'area': a[validos]})

matriz = trans.pivot_table(index='de', columns='para', values='area',
                           aggfunc='sum', fill_value=0).round(0)
matriz.to_csv(f'{BASE}/resultados/matriz_transicao_1990_2020.csv')
matriz
```

```python
area_total = matriz.values.sum()
area_mudou = area_total - np.trace(matriz.reindex(columns=matriz.index, fill_value=0).values)
print(f'Área que mudou de classe: {area_mudou:,.0f} km² ({100 * area_mudou / area_total:.1f}%)')
```

> 💡 Ao escrever, destaque as **maiores transições** (ex.: "X km² passaram de Cwa para Aw").

---

## 11.6 Mapa das mudanças

```python
mudou = (koppen.sel(ano=1990) != koppen.sel(ano=2020)) & (koppen.sel(ano=1990) > 0)

# Ano da última mudança de classe em cada pixel
diferente = koppen != koppen.shift(ano=1)
ultimo_ano = diferente.where(diferente).ano.where(diferente).max('ano')

fig, axs = plt.subplots(1, 2, figsize=(14, 6))
mudou.where(koppen.sel(ano=1990) > 0).plot(ax=axs[0], cmap='Reds', add_colorbar=False)
axs[0].set_title('Pixels que mudaram de classe (1990 → 2020)')
ultimo_ano.where(mudou).plot(ax=axs[1], cmap='viridis')
axs[1].set_title('Ano da última mudança')
plt.show()
fig.savefig(f'{BASE}/figuras/mapa_mudancas.png', dpi=300, bbox_inches='tight')
```

### Contorno do Brasil e dos estados

```python
!pip install geobr
import geobr

estados = geobr.read_state(year=2020)

fig, ax = plt.subplots(figsize=(8, 8))
mudou.where(koppen.sel(ano=1990) > 0).plot(ax=ax, cmap='Reds', add_colorbar=False)
estados.boundary.plot(ax=ax, color='black', linewidth=0.4)
ax.set_title('Mudança de classe de Köppen (1961–1990 → 1991–2020)')
plt.show()
```

---

## 11.7 Tendência pixel a pixel

Mesmo princípio do Capítulo 8: **série anual**, nunca janelas móveis.

```python
import pymannkendall as mk

tmed_anual = tmed.resample(time='YS').mean()        # cubos do Capítulo 10
chuva_anual = chuva.resample(time='YS').sum(min_count=12)


def sen_e_p(serie):
    if np.isnan(serie).any():
        return np.nan, np.nan
    r = mk.original_test(serie)
    return r.slope * 10, r.p          # por década


def tendencia_grade(da):
    sen, p = xr.apply_ufunc(sen_e_p, da, input_core_dims=[['time']],
                            output_core_dims=[[], []], vectorize=True)
    return sen, p


sen_t, p_t = tendencia_grade(tmed_anual)
sen_p, p_p = tendencia_grade(chuva_anual)

xr.Dataset({'sen_T': sen_t, 'p_T': p_t, 'sen_P': sen_p, 'p_P': p_p}) \
  .to_netcdf(f'{saida}/tendencias_grade.nc')
```

> ⏳ Pode demorar bastante (um teste por pixel). Teste antes num recorte pequeno, por exemplo o Paraná.

```python
fig, ax = plt.subplots(figsize=(8, 8))
sen_t.plot(ax=ax, cmap='Reds', cbar_kwargs={'label': '°C/década'})
(p_t < 0.05).where(p_t < 0.05).plot.contourf(ax=ax, levels=[0.5, 1.5], hatches=['..'],
                                             colors='none', add_colorbar=False)
estados.boundary.plot(ax=ax, color='black', linewidth=0.4)
ax.set_title('Tendência de Tmed (pontilhado = p < 0,05)')
plt.show()
```

> ⚠️ Com milhares de testes, alguns pixels serão "significativos" por acaso (cerca de 5%). Discuta isso com o orientador; uma opção é o controle da taxa de falsas descobertas (FDR).

---

## 11.8 Interpretação

Ao discutir os resultados, relacione sempre:
- **mudança de classe** (Köppen e demais) × **tendência** (Mann-Kendall/Sen);
- regiões com mudança × **densidade de estações** do Xavier (Capítulo 4);
- concordância entre classificações (Capítulo 9);
- seus resultados × literatura (ex.: Alvares et al., 2013, e estudos de tendência no Brasil).

---

## 11.9 Redação

Estrutura sugerida:

1. **Introdução:** mudança climática, importância das classificações, lacuna (classificações em períodos fixos).
2. **Material e Métodos:** base do Xavier; clima de referência móvel; classificações; Mann-Kendall e Sen na série anual; Fase A e Fase B.
3. **Resultados:** 27 capitais; área por classe; matriz de transição; mapas de mudança e de tendência.
4. **Discussão:** comparação com a literatura e limitações (Capítulo 4, representatividade dos pontos, testes múltiplos).
5. **Conclusão:** responda à pergunta do Capítulo 1: *onde, quanto e desde quando*.

Referências em **ABNT**. Toda referência deve ser conferida na fonte original.

---

## 11.10 Publicando o código

Organize um repositório no GitHub:

```
mudanca_climatica_br/
├── README.md          → objetivo, dados, como reproduzir
├── notebooks/         → cap02 a cap11, limpos e comentados
├── resultados/        → tabelas finais (CSV)
└── figuras/           → figuras finais
```

> 💡 Antes de publicar, rode cada notebook do início ao fim e remova células de teste.

---

## 11.11 Resumo para evento

Para um evento como o SICITE, escreva um resumo com:
- objetivo (1 frase);
- métodos (2 a 3 frases);
- 2 ou 3 resultados com **números** (ex.: % de área que mudou, maior transição, tendência média de temperatura);
- conclusão (1 frase).

---

## 11.12 Exercícios

1. Qual classe ganhou mais área entre 1990 e 2020? Qual perdeu mais?
2. Qual foi a maior transição da matriz, em km²?
3. Que porcentagem do Brasil mudou de classe?
4. As regiões com mudança de classe coincidem com as de tendência significativa de temperatura?
5. Escreva o rascunho do resumo para evento.

---

## ✅ Checklist do Capítulo 11

- [ ] Calculei a área por classe com a área correta de cada pixel
- [ ] Montei a matriz de transição 1990 → 2020
- [ ] Fiz os mapas de mudança e do ano da última mudança
- [ ] Calculei e mapeei as tendências pixel a pixel
- [ ] Escrevi o texto com a estrutura da seção 11.9
- [ ] Publiquei os notebooks no GitHub
- [ ] Escrevi o resumo para evento

**Entregável 11:** relatório final + resumo para evento + repositório no GitHub com os notebooks.
