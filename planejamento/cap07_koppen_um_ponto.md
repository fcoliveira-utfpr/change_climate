# Capítulo 7 — Clima de Referência Móvel e Köppen em um Ponto

> **Objetivo do capítulo:** aplicar o método completo em Santa Helena-PR: calcular o clima de cada ano (janela de 30 anos), classificá-lo por Köppen e identificar se e quando a classe mudou.
> Notebook: `cap07_koppen_um_ponto.ipynb`

---

## 7.1 O que vamos construir

```
série mensal (Cap. 5)
   → para cada ano de 1990 a 2020:
        janela de 30 anos → 12 médias mensais → classe de Köppen
   → tabela: ano | tmed | chuva | classe
   → anos em que a classe mudou
```

Tudo em **funções**, para reaproveitar nos 27 pontos (Cap. 8) e na grade (Cap. 10).

---

## 7.2 Carregando a série e as funções do Capítulo 3

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

mensal = pd.read_csv(f'{BASE}/dados/xavier_santa_helena_mensal_gee.csv',
                     index_col='data', parse_dates=True)


def janela_30_anos(ano):
    """Ano inicial e final da janela de 30 anos que termina em `ano`."""
    return ano - 29, ano


def clima_do_periodo(mensal, ano_ini, ano_fim):
    """12 médias mensais (chuva e tmed) entre ano_ini e ano_fim."""
    periodo = mensal.loc[str(ano_ini):str(ano_fim)]
    return periodo.groupby(periodo.index.month).mean()
```

---

## 7.3 Revisando as regras de Köppen

Usamos os critérios adotados por Alvares et al. (2013) para o Brasil. No Hemisfério Sul, o **verão** é de outubro a março e o **inverno**, de abril a setembro.

| Símbolo | Regra (simplificada) |
|---|---|
| **B** (seco) | chuva anual < limiar de aridez, calculado a partir da temperatura e da distribuição da chuva |
| **A** (tropical) | mês mais frio ≥ 18 °C |
| **C** (temperado) | mês mais frio < 18 °C |
| **Af** | mês mais seco ≥ 60 mm |
| **Am** | mês mais seco < 60 mm e ≥ 100 − (chuva anual / 25) |
| **Aw / As** | estação seca no inverno / no verão |
| **Cf / Cw / Cs** | sem estação seca / inverno seco / verão seco |
| **a / b** | mês mais quente ≥ 22 °C / < 22 °C |

---

## 7.4 Classificando com a agrometeorologiapy

A classificação oficial do projeto é feita pela **agrometeorologiapy**:

```python
import agrometeorologiapy as agp

clima_2000 = clima_do_periodo(mensal, *janela_30_anos(2000))

classe = <<FUNÇÃO: Köppen>>(clima_2000['tmed'].values,
                            clima_2000['chuva'].values)
print('Clima de 2000 (1971–2000):', classe)
```

> ⚠️ O nome exato da função e a ordem dos argumentos serão informados pelo orientador. Consulte a documentação da biblioteca: https://github.com/fcoliveira-utfpr/agrometeorologiapy

---

## 7.5 Uma versão própria, para conferência

Escrever a regra você mesma é a melhor forma de entender Köppen e serve para **conferir** a biblioteca.

```python
VERAO = [10, 11, 12, 1, 2, 3]     # Hemisfério Sul
INVERNO = [4, 5, 6, 7, 8, 9]


def koppen_simples(t, p):
    """
    t, p: pandas Series com 12 valores (índice = mês 1..12).
    Retorna a classe de Köppen (versão didática para o Brasil).
    """
    t_ano, p_ano = t.mean(), p.sum()
    t_frio, t_quente = t.min(), t.max()

    # Grupo B: limiar de aridez
    frac_verao = p[VERAO].sum() / p_ano
    if frac_verao >= 0.7:
        limiar = 20 * t_ano + 280
    elif frac_verao >= 0.3:
        limiar = 20 * t_ano + 140
    else:
        limiar = 20 * t_ano
    if p_ano < limiar:
        return 'BWh' if p_ano < limiar / 2 else 'BSh'

    # Grupo A
    if t_frio >= 18:
        p_seco = p.min()
        if p_seco >= 60:
            return 'Af'
        if p_seco >= 100 - p_ano / 25:
            return 'Am'
        return 'As' if p[VERAO].min() < p[INVERNO].min() else 'Aw'

    # Grupo C
    terceira = 'a' if t_quente >= 22 else 'b'
    if p[INVERNO].min() < p[VERAO].max() / 10:
        segunda = 'w'
    elif p[VERAO].min() < 40 and p[VERAO].min() < p[INVERNO].max() / 3:
        segunda = 's'
    else:
        segunda = 'f'
    return 'C' + segunda + terceira


print(koppen_simples(clima_2000['tmed'], clima_2000['chuva']))
```

> 🧠 Compare com o resultado da agrometeorologiapy. Se forem diferentes, descubra **qual regra** causou a diferença e anote.

---

## 7.6 Classificando todos os anos

```python
def classes_por_ano(mensal, ano_ini=1990, ano_fim=2020, classificar=koppen_simples):
    """Tabela com o clima de referência móvel e a classe de cada ano."""
    linhas = []
    for ano in range(ano_ini, ano_fim + 1):
        ini, fim = janela_30_anos(ano)
        clima = clima_do_periodo(mensal, ini, fim)
        linhas.append({
            'ano': ano,
            'periodo': f'{ini}-{fim}',
            'tmed': clima['tmed'].mean(),
            'chuva': clima['chuva'].sum(),
            't_mes_frio': clima['tmed'].min(),
            't_mes_quente': clima['tmed'].max(),
            'p_mes_seco': clima['chuva'].min(),
            'classe': classificar(clima['tmed'], clima['chuva']),
        })
    return pd.DataFrame(linhas).set_index('ano').round(2)


res = classes_por_ano(mensal)
res
```

> 💡 O parâmetro `classificar` permite trocar a função de classificação (sua versão ou a da biblioteca) sem mudar o resto do código.
> 💡 As colunas `t_mes_frio`, `t_mes_quente` e `p_mes_seco` mostram **o quanto** o clima está perto de mudar de classe, mesmo quando a classe não muda.

---

## 7.7 Quando a classe mudou?

```python
mudou = res['classe'] != res['classe'].shift()
mudancas = res.loc[mudou, ['periodo', 'classe']].iloc[1:]   # ignora o 1º ano

if mudancas.empty:
    print('A classe não mudou entre 1990 e 2020:', res['classe'].iloc[0])
else:
    print(mudancas)
```

> 🧠 Se a classe muda e volta no ano seguinte (ex.: Cfa → Cwa → Cfa), o clima está **perto de um limiar**. Mudança consistente é a que **permanece**.

---

## 7.8 Gráficos

```python
fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

axs[0].plot(res.index, res['tmed'], marker='o', color='red')
axs[0].set_ylabel('Tmed (°C)')

axs[1].plot(res.index, res['chuva'], marker='o', color='steelblue')
axs[1].set_ylabel('Chuva (mm/ano)')

axs[2].plot(res.index, res['t_mes_quente'], marker='o', color='orange')
axs[2].axhline(22, ls='--', color='gray')       # limiar a/b
axs[2].set_ylabel('T mês mais quente (°C)')
axs[2].set_xlabel('Ano (fim da janela de 30 anos)')

for ax in axs:
    ax.grid(alpha=0.3)
fig.suptitle('Clima de referência móvel — Santa Helena-PR (Xavier)')
plt.show()

fig.savefig(f'{BASE}/figuras/clima_movel_santa_helena.png', dpi=300, bbox_inches='tight')
res.to_csv(f'{BASE}/resultados/koppen_santa_helena.csv')
```

> ⚠️ **Não aplique teste de tendência a estas curvas.** Janelas vizinhas compartilham 29 anos, então os valores não são independentes. A estatística de tendência é feita na **série anual** (Capítulo 8).

---

## 7.9 Exercícios

1. Qual a classe de Santa Helena em 1990 e em 2020? Mudou?
2. Quanto a temperatura média do clima variou entre a janela de 1990 e a de 2020? E a chuva?
3. Qual critério está mais perto de provocar uma mudança de classe? Use as colunas `t_mes_frio`, `t_mes_quente` e `p_mes_seco`.
4. Compare sua função `koppen_simples` com a da agrometeorologiapy em todos os anos. Houve diferenças?
5. Explique por que não se deve aplicar Mann-Kendall à série das janelas móveis.

---

## ✅ Checklist do Capítulo 7

- [ ] Classifiquei o clima de um ano com a agrometeorologiapy
- [ ] Escrevi e testei a função `koppen_simples`
- [ ] Criei a função `classes_por_ano` e gerei a tabela 1990–2020
- [ ] Identifiquei os anos de mudança de classe
- [ ] Fiz e salvei os gráficos e a tabela de resultados
- [ ] Respondi os exercícios

**Entregável 7:** notebook `cap07_koppen_um_ponto.ipynb` + `koppen_santa_helena.csv` + figura do clima móvel + comparação biblioteca × função própria.
