# Capítulo 8 — Escalando para 27 Pontos + Estatística de Tendência

> **Objetivo do capítulo:** aplicar o método do Capítulo 7 às 27 capitais, resumir as mudanças de classe e testar estatisticamente as tendências de temperatura e chuva.
> Notebook: `cap08_27_pontos_estatistica.ipynb`

---

## 8.1 Duas perguntas diferentes

| Pergunta | Ferramenta | Série usada |
|---|---|---|
| A **classe** do clima mudou? | clima de referência móvel + Köppen | janelas de 30 anos (Cap. 7) |
| Há **tendência** significativa? | Mann-Kendall + declividade de Sen | **série anual** (um valor por ano) |

> ⚠️ **Ponto metodológico central:** testes de tendência exigem valores (aproximadamente) independentes. As janelas móveis compartilham 29 de 30 anos, então são fortemente autocorrelacionadas e dariam "significância" falsa. Por isso, **Mann-Kendall e Sen são aplicados à série anual**, nunca às janelas.

---

## 8.2 Preparação

Copie para o notebook as funções `janela_30_anos`, `clima_do_periodo`, `koppen_simples` e `classes_por_ano` (Cap. 7).

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mk

pontos = pd.read_csv(f'{BASE}/dados/pontos_27_capitais.csv')
pasta = f'{BASE}/dados/series_27'

REGIAO = {
    'AC': 'Norte', 'AM': 'Norte', 'AP': 'Norte', 'PA': 'Norte',
    'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste',
    'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste',
    'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'MT': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul',
}
pontos['regiao'] = pontos['uf'].map(REGIAO)
```

---

## 8.3 Classificando os 27 pontos

```python
def ler_serie(uf):
    return pd.read_csv(f'{pasta}/{uf}.csv', index_col='data', parse_dates=True)


tabelas = {}
for uf in pontos['uf']:
    tabelas[uf] = classes_por_ano(ler_serie(uf))
    tabelas[uf].to_csv(f'{BASE}/resultados/koppen_{uf}.csv')

print('Classificados:', len(tabelas))
```

### Resumo das mudanças de classe

```python
linhas = []
for uf, res in tabelas.items():
    mudou = (res['classe'] != res['classe'].shift()).iloc[1:]
    linhas.append({
        'uf': uf,
        'classe_1990': res['classe'].iloc[0],
        'classe_2020': res['classe'].iloc[-1],
        'n_mudancas': int(mudou.sum()),
        'dT_clima': res['tmed'].iloc[-1] - res['tmed'].iloc[0],     # 1991–2020 menos 1961–1990
        'dP_clima': res['chuva'].iloc[-1] - res['chuva'].iloc[0],
    })

resumo = pontos.merge(pd.DataFrame(linhas), on='uf').round(2)
resumo['mudou'] = resumo['classe_1990'] != resumo['classe_2020']
resumo
```

> 💡 A janela de 1990 é 1961–1990 e a de 2020 é 1991–2020: elas **não se sobrepõem**, então `dT_clima` e `dP_clima` comparam dois climas independentes.

---

## 8.4 Mann-Kendall e declividade de Sen

- **Mann-Kendall:** testa se há tendência monotônica (sempre subindo ou sempre descendo), sem supor distribuição normal. Resultado: `p-valor`; se p < 0,05, a tendência é significativa.
- **Declividade de Sen:** estima a **magnitude** da tendência (mediana das inclinações entre todos os pares de anos). Resistente a valores extremos.

Exemplo em um ponto:

```python
df = ler_serie('PR')
anual_t = df['tmed'].resample('YS').mean()
anual_p = df['chuva'].resample('YS').sum()

r = mk.original_test(anual_t)
print(r.trend, f'p = {r.p:.4f}', f'Sen = {r.slope * 10:.3f} °C/década')
```

> 🧠 Séries anuais de clima também podem ter alguma autocorrelação. Compare com `mk.hamed_rao_modification_test`, que corrige esse efeito. Se os resultados forem diferentes, discuta com o orientador.

### Aplicando aos 27 pontos

```python
def tendencia(serie):
    r = mk.original_test(serie)
    r2 = mk.hamed_rao_modification_test(serie)
    return r.slope * 10, r.p, r2.p        # Sen por década


linhas = []
for uf in pontos['uf']:
    df = ler_serie(uf)
    sen_t, p_t, p_t_hr = tendencia(df['tmed'].resample('YS').mean())
    sen_p, p_p, p_p_hr = tendencia(df['chuva'].resample('YS').sum())
    linhas.append({'uf': uf,
                   'sen_T_dec': sen_t, 'p_T': p_t, 'p_T_HR': p_t_hr,
                   'sen_P_dec': sen_p, 'p_P': p_p, 'p_P_HR': p_p_hr})

tend = pd.DataFrame(linhas)
resultados = resumo.merge(tend, on='uf').round(4)
resultados['sig_T'] = resultados['p_T'] < 0.05
resultados['sig_P'] = resultados['p_P'] < 0.05

resultados.to_csv(f'{BASE}/resultados/resultados_27_pontos.csv', index=False)
resultados[['uf', 'classe_1990', 'classe_2020', 'sen_T_dec', 'sig_T', 'sen_P_dec', 'sig_P']]
```

---

## 8.5 Mapas dos resultados

```python
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Tendência de temperatura
sc = axs[0].scatter(resultados['lon'], resultados['lat'],
                    c=resultados['sen_T_dec'], cmap='Reds', s=120,
                    edgecolor=np.where(resultados['sig_T'], 'black', 'none'),
                    linewidth=1.5)
plt.colorbar(sc, ax=axs[0], label='°C/década')
axs[0].set_title('Tendência de Tmed (borda preta = p < 0,05)')

# Tendência de chuva
sc = axs[1].scatter(resultados['lon'], resultados['lat'],
                    c=resultados['sen_P_dec'], cmap='BrBG', s=120,
                    vmin=-abs(resultados['sen_P_dec']).max(),
                    vmax=abs(resultados['sen_P_dec']).max(),
                    edgecolor=np.where(resultados['sig_P'], 'black', 'none'),
                    linewidth=1.5)
plt.colorbar(sc, ax=axs[1], label='mm/ano por década')
axs[1].set_title('Tendência de chuva (borda preta = p < 0,05)')

for ax, (_, p) in [(ax, p) for ax in axs for p in resultados.iterrows()]:
    ax.annotate(p['uf'], (p['lon'], p['lat']), fontsize=7,
                xytext=(4, 4), textcoords='offset points')

for ax in axs:
    ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude'); ax.set_aspect('equal')
plt.tight_layout()
plt.show()
fig.savefig(f'{BASE}/figuras/tendencias_27_pontos.png', dpi=300, bbox_inches='tight')
```

> 💡 No Capítulo 11, faremos mapas com o contorno do Brasil. Por enquanto, a dispersão lat × lon basta para enxergar o padrão.

---

## 8.6 Resumo por região

```python
por_regiao = resultados.groupby('regiao').agg(
    pontos=('uf', 'count'),
    mudaram_classe=('mudou', 'sum'),
    dT_clima_medio=('dT_clima', 'mean'),
    sen_T_medio=('sen_T_dec', 'mean'),
    pontos_sig_T=('sig_T', 'sum'),
    sen_P_medio=('sen_P_dec', 'mean'),
    pontos_sig_P=('sig_P', 'sum'),
).round(2)

por_regiao
por_regiao.to_csv(f'{BASE}/resultados/resumo_por_regiao.csv')
```

---

## 8.7 Interpretando com cuidado

- **Tendência significativa ≠ mudança de classe.** Um ponto pode aquecer muito sem cruzar nenhum limiar de Köppen, e outro pode mudar de classe com pouco aquecimento por estar perto de um limiar.
- **Chuva é mais variável** que temperatura: tendências de chuva costumam ser menos significativas.
- **Lembre do Capítulo 4:** em regiões com poucas estações (Norte), parte da tendência pode vir de mudanças na rede de observação.
- **27 pontos ≠ 27 estados:** os resultados descrevem as capitais.

---

## 8.8 Exercícios

1. Quantas capitais mudaram de classe entre 1990 e 2020? Quais e para quais classes?
2. Em quantas a tendência de temperatura foi significativa? E a de chuva?
3. Qual região aqueceu mais, segundo a declividade de Sen?
4. Os resultados do teste original e do teste de Hamed e Rao diferiram em algum ponto? Por que isso pode acontecer?
5. Encontre uma capital com tendência significativa de aquecimento que **não** mudou de classe e explique por quê.

---

## ✅ Checklist do Capítulo 8

- [ ] Classifiquei os 27 pontos e salvei uma tabela por capital
- [ ] Montei o resumo das mudanças de classe
- [ ] Apliquei Mann-Kendall e Sen à **série anual** dos 27 pontos
- [ ] Salvei `resultados_27_pontos.csv` e `resumo_por_regiao.csv`
- [ ] Fiz os mapas de tendência
- [ ] Respondi os exercícios

**Entregável 8:** notebook `cap08_27_pontos_estatistica.ipynb` + `resultados_27_pontos.csv` + `resumo_por_regiao.csv` + mapas de tendência.
