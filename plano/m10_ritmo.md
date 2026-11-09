# Missão 10: O ritmo da mudança, ou quantos anos faltam

> **Pergunta da missão:** no ritmo atual, em quantos anos cada critério cruza o limiar?
> **Duração:** 3 semanas
> **Notebook:** `m09_ritmo.ipynb`
> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com)
> 📓 **Notebook de exemplo:** [Exemplo 11: Tendência e ritmo (abrir no Colab)](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/11_tendencia_ritmo.ipynb). O exemplo é feito para Santa Helena (e Curitiba); na seção ✍️ **Sua vez**, você repete para as capitais.
> **Fim da fase 2:** nesta missão você escreve o **relatório parcial**

---

## Por que isso importa

Uma folga de −0,5 °C pode ser "pouco" ou "muito". Depende do **ritmo**: se o mês mais frio esquenta
0,3 °C por década, faltam cerca de 17 anos; se esquenta 0,05 °C por década, faltam 100 anos.

**Anos até cruzar = folga ÷ ritmo**

Para medir o ritmo, usamos dois métodos clássicos em climatologia:

- **Teste de Mann-Kendall:** diz se existe uma **tendência** (sempre subindo ou sempre descendo) ou se as
  variações são só acaso. Resultado: o **p-valor**. Se p < 0,05, a tendência é considerada significativa.
- **Declividade de Sen:** estima **quanto** a variável muda por ano. É a mediana das inclinações entre todos
  os pares de anos, por isso não se deixa levar por um ano extremo.

> ⚠️ **Ponto central do método:** o teste é aplicado à **série anual** (um valor por ano, de 1961 a 2025),
> e **nunca** à curva da janela móvel. Na janela móvel, anos vizinhos compartilham 29 de 30 anos, e o teste
> acharia "tendência" em qualquer coisa.

## O que você vai aprender de Python

- usar uma biblioteca de **estatística** pronta (`pymannkendall`);
- usar `if` para tomar uma decisão no código.

---

## Semana 1: a série anual de cada critério

Para cada critério, precisamos de um valor **por ano**. Por exemplo, para a folga A/C, usamos a temperatura
do mês mais frio **de cada ano**.

```python
from google.colab import drive
drive.mount('/content/drive')
!pip install agrometeorologiapy pymannkendall

import agrometeorologiapy as amp
import pymannkendall as mk
import pandas as pd
import matplotlib.pyplot as plt

BASE = '/content/drive/MyDrive/mudanca_climatica_br'
LATITUDE = -24.86
serie = pd.read_csv(f'{BASE}/dados/santa_helena_mensal.csv', parse_dates=['data'], index_col='data')
```

```python
# Temperatura do mês mais FRIO de cada ano: o menor dos 12 meses de cada ano
t_mes_frio_anual = serie['tmed'].resample('YS').min()

# Temperatura do mês mais QUENTE de cada ano
t_mes_quente_anual = serie['tmed'].resample('YS').max()

# Chuva do mês mais SECO de cada ano
p_mes_seco_anual = serie['chuva'].resample('YS').min()

t_mes_frio_anual.head()
```

Faça um gráfico simples de `t_mes_frio_anual` (anos no eixo x) com a linha do limiar de 18 °C. Repare como
ele varia muito mais de um ano para o outro do que a curva da janela móvel.

> 💭 **Para pensar e levar ao encontro:** a média de `t_mes_frio_anual` é um pouco **menor** que a
> temperatura do mês mais frio da normal. Por quê? (Dica: o mês mais frio nem sempre é o mesmo em todos os
> anos.) Uma alternativa é usar sempre o mesmo mês, por exemplo julho:
> `serie['tmed'][serie.index.month == 7]`. Compare os dois ritmos.

---

## Semana 2: Mann-Kendall e Sen

```python
# Aplica o teste à série anual do mês mais frio
teste = mk.original_test(t_mes_frio_anual)

# O teste devolve vários valores. Os que importam para nós:
#   teste.trend -> 'increasing' (subindo), 'decreasing' (descendo) ou 'no trend' (sem tendência)
#   teste.p     -> o p-valor
#   teste.slope -> a declividade de Sen, em °C POR ANO
print('Tendência:', teste.trend)
print('p-valor:', round(teste.p, 4))

# Multiplicamos por 10 para ter o ritmo por DÉCADA, que é mais fácil de ler
ritmo_por_decada = teste.slope * 10
print('Ritmo:', round(ritmo_por_decada, 3), '°C por década')
```

> 🧠 Séries climáticas anuais às vezes têm "memória": um ano quente tende a ser seguido por outro quente.
> Isso pode enganar o teste. O teste de **Hamed e Rao** corrige esse efeito. Compare:

```python
teste_corrigido = mk.hamed_rao_modification_test(t_mes_frio_anual)
print('p-valor original:', round(teste.p, 4))
print('p-valor corrigido:', round(teste_corrigido.p, 4))
```

Repita o teste para `t_mes_quente_anual` e `p_mes_seco_anual`.

---

## Semana 3: quantos anos faltam?

```python
# Folga atual: a do clima de 1996-2025 (última janela da Missão 8 ou 8)
resultado = pd.read_csv(f'{BASE}/resultados/janela_movel_santa_helena.csv', index_col='ano')
folga_atual = resultado.loc[2025, 'folga_A']

# Ritmo por ano (declividade de Sen)
ritmo = teste.slope

print('Folga atual (°C):', round(folga_atual, 2))
print('Ritmo (°C/ano):', round(ritmo, 4))

# Há quatro situações possíveis:
#   1) abaixo do limiar (folga negativa) e subindo (ritmo positivo)  -> vai cruzar para cima
#   2) acima do limiar (folga positiva) e descendo (ritmo negativo)  -> vai cruzar para baixo
#   3) acima do limiar e subindo  -> se afasta do limiar (talvez já tenha cruzado no passado!)
#   4) abaixo do limiar e descendo -> se afasta do limiar
if folga_atual < 0 and ritmo > 0:
    anos_ate_cruzar = -folga_atual / ritmo
    print('Abaixo do limiar e subindo: cruza em cerca de', round(anos_ate_cruzar), 'anos')
elif folga_atual > 0 and ritmo < 0:
    anos_ate_cruzar = folga_atual / -ritmo
    print('Acima do limiar e descendo: cruza em cerca de', round(anos_ate_cruzar), 'anos')
elif folga_atual > 0 and ritmo > 0:
    print('Acima do limiar e subindo: está se afastando do limiar.')
    print('Confira na Missão 8 se ele já cruzou esse limiar em algum ano.')
else:
    print('Abaixo do limiar e descendo (ou sem mudança): está se afastando do limiar.')
```

> ⚠️ **Cuidado na interpretação.** Isso é uma **extrapolação**: supõe que o ritmo de 1961–2025 continue
> igual. Use frases como "no ritmo observado, cruzaria em cerca de X anos", nunca "vai mudar em X anos". E
> só faz sentido falar em ritmo se a tendência for significativa.

Monte uma tabela com os critérios de Köppen: **folga atual, ritmo por década, p-valor e anos até cruzar**.
Salve em `resultados/ritmo_santa_helena.csv`.

### Desafio opcional: o ritmo do Im

O Im de Thornthwaite também pode ser calculado **para cada ano** (com os 12 meses daquele ano, sem janela):

```python
linhas = []
for ano in range(1961, 2026):
    # Os 12 meses de um único ano
    um_ano = serie.loc[str(ano)]
    temperatura = um_ano['tmed'].tolist()
    chuva = um_ano['chuva'].tolist()

    # Thornthwaite do ano
    tabela_etp = amp.thornthwaite_mensal(pd.DataFrame({'T_media_C': temperatura}), lat=LATITUDE)
    thornthwaite = amp.classificacao_thornthwaite(chuva, tabela_etp['ETP_mm_mes'], LATITUDE)

    linhas.append({'ano': ano, 'Im': thornthwaite['Im']})

im_anual = pd.DataFrame(linhas).set_index('ano')['Im']
```

Aplique Mann-Kendall e Sen a `im_anual`. O Im está diminuindo, ou seja, o clima está ficando mais seco?

---

## 📝 Relatório parcial: fim da fase 2

Escreva de **3 a 5 páginas**, com esta estrutura:

1. **Introdução** (meia página): mudança climática, classificações climáticas e a ideia de folga.
2. **Material e métodos** (1 página): dados do Xavier; Köppen e Thornthwaite (com a biblioteca); clima de
   referência móvel; folgas; Mann-Kendall e Sen na série anual.
3. **Resultados** (1 a 2 páginas): as duas normais (M7), a janela móvel (M8), Curitiba (M9) e o ritmo (M10).
   Use as suas figuras e tabelas.
4. **Próximos passos** (meia página): o que vem na fase 3.

O orientador vai revisar o texto com você. Isso é normal e faz parte de aprender a escrever ciência.

## 📦 Entregável

- ✍️ A seção **Sua vez** do notebook de exemplo, feita para as capitais pedidas.
- `resultados/ritmo_santa_helena.csv`.
- O relatório parcial.

## 🗣️ Para o próximo encontro, saiba responder

- O que o teste de Mann-Kendall testa? O que é a declividade de Sen?
- Por que o teste vai na série anual e não na janela móvel?
- Por que "anos até cruzar" é uma extrapolação, e qual o cuidado ao escrever sobre isso?

## ✅ Checklist

- [ ] Montei as séries anuais dos critérios
- [ ] Apliquei Mann-Kendall, Sen e Hamed-Rao
- [ ] Calculei os anos até cruzar e montei a tabela
- [ ] Escrevi o relatório parcial
- [ ] Preenchi o diário de bordo
