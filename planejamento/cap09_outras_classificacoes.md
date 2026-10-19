# Capítulo 9 — Outras Classificações: Thornthwaite, Camargo e Holdridge

> **Objetivo do capítulo:** aplicar outras três classificações ao clima de referência móvel e comparar a sensibilidade de cada uma para detectar mudanças.
> Notebook: `cap09_outras_classificacoes.ipynb`

---

## 9.1 Por que usar mais de uma classificação?

Cada classificação "enxerga" o clima de um jeito:

| Classificação | Baseia-se em | Sensível a |
|---|---|---|
| **Köppen** | temperatura e chuva mensais, com limiares fixos | cruzamento de limiares (18 °C, 22 °C, 60 mm...) |
| **Thornthwaite** | balanço hídrico (chuva × ETP) | disponibilidade de água |
| **Camargo** | balanço hídrico, adaptado ao Brasil | deficiência hídrica e temperatura, com foco agrícola |
| **Holdridge** | biotemperatura e chuva anual (escala logarítmica) | grandes mudanças ligadas à vegetação |

> 🧠 Se várias classificações apontam mudança no mesmo lugar, a evidência é mais forte. Se só uma aponta, pode ser efeito de um limiar específico.

---

## 9.2 Conceitos novos

**Evapotranspiração potencial (ETP):** quanta água a atmosfera "pediria" de uma superfície vegetada sem falta de água. Pelo método de Thornthwaite, depende só da temperatura e do comprimento do dia (latitude).

**Balanço hídrico climatológico:** compara, mês a mês, a chuva (entrada) com a ETP (saída), considerando a água que o solo consegue armazenar (CAD, capacidade de água disponível, geralmente 100 mm). Resultados principais:
- **DEF (deficiência):** água que faltou
- **EXC (excedente):** água que sobrou

**Índices de Thornthwaite (1948):**
- Índice hídrico: Ih = 100 · EXC / ETP
- Índice de aridez: Ia = 100 · DEF / ETP
- Índice de umidade: Im = Ih − 0,6 · Ia

**Biotemperatura (Holdridge):** média das temperaturas considerando apenas valores entre 0 °C e 30 °C (fora dessa faixa, a vegetação praticamente não cresce).

> ⚠️ Confira as equações e os coeficientes nas referências originais e na documentação da agrometeorologiapy antes de usar.

---

## 9.3 Classificando com a agrometeorologiapy

Mesma estrutura do Capítulo 7: só trocamos a função de classificação.

```python
import pandas as pd
import agrometeorologiapy as agp

LAT = -24.86   # Santa Helena (Thornthwaite e Camargo precisam da latitude)


def classe_thornthwaite(t, p):
    return <<FUNÇÃO: Thornthwaite>>(t.values, p.values, LAT)


def classe_camargo(t, p):
    return <<FUNÇÃO: Camargo>>(t.values, p.values, LAT)


def classe_holdridge(t, p):
    return <<FUNÇÃO: Holdridge>>(t.values, p.values)
```

> ⚠️ Os nomes e argumentos das funções serão informados pelo orientador. Verifique também se a CAD é um argumento e use **100 mm** como padrão.

---

## 9.4 Uma conferência simples: biotemperatura

```python
def biotemperatura(t):
    """Biotemperatura média anual (°C) a partir das 12 temperaturas mensais."""
    t_bio = t.where((t > 0) & (t < 30), 0)
    return t_bio.mean()
```

> 🧠 Com dados mensais, a biotemperatura é uma aproximação: um mês com média de 25 °C pode ter dias acima de 30 °C. Em capitais muito quentes, compare com o valor da biblioteca.

---

## 9.5 Aplicando as quatro classificações

A função `classes_por_ano` do Capítulo 7 já aceita outra classificação pelo parâmetro `classificar`. Basta chamá-la várias vezes:

```python
mensal = pd.read_csv(f'{BASE}/dados/xavier_santa_helena_mensal_gee.csv',
                     index_col='data', parse_dates=True)

CLASSIFICACOES = {
    'koppen': koppen_simples,          # ou a função da biblioteca
    'thornthwaite': classe_thornthwaite,
    'camargo': classe_camargo,
    'holdridge': classe_holdridge,
}

comp = pd.DataFrame({
    nome: classes_por_ano(mensal, classificar=func)['classe']
    for nome, func in CLASSIFICACOES.items()
})
comp
```

---

## 9.6 Comparando a sensibilidade

```python
def resumo_mudancas(classes):
    """Número de mudanças e classes inicial e final de uma série de classes."""
    mudou = (classes != classes.shift()).iloc[1:]
    return pd.Series({
        'classe_1990': classes.iloc[0],
        'classe_2020': classes.iloc[-1],
        'n_mudancas': int(mudou.sum()),
        'anos_mudanca': list(classes.index[1:][mudou.values]),
    })


comp.apply(resumo_mudancas).T
```

Para as 27 capitais (use a latitude de cada ponto):

```python
pontos = pd.read_csv(f'{BASE}/dados/pontos_27_capitais.csv')
linhas = []

for _, pt in pontos.iterrows():
    LAT = pt['lat']                    # atualiza a latitude usada pelas funções
    m = ler_serie(pt['uf'])
    for nome, func in CLASSIFICACOES.items():
        r = resumo_mudancas(classes_por_ano(m, classificar=func)['classe'])
        linhas.append({'uf': pt['uf'], 'classificacao': nome,
                       'mudou': r['classe_1990'] != r['classe_2020'],
                       'n_mudancas': r['n_mudancas'],
                       'de': r['classe_1990'], 'para': r['classe_2020']})

sens = pd.DataFrame(linhas)
sens.to_csv(f'{BASE}/resultados/comparacao_classificacoes_27.csv', index=False)

# Em quantas capitais cada classificação detectou mudança?
sens.groupby('classificacao')['mudou'].sum()
```

```python
# Concordância: em quantas classificações cada capital mudou?
concordancia = sens.groupby('uf')['mudou'].sum().sort_values(ascending=False)
concordancia
```

> 💡 Capitais em que 3 ou 4 classificações indicam mudança são os casos mais robustos para discutir no trabalho.

---

## 9.7 Exercícios

1. Explique com suas palavras a diferença entre ETP e chuva, e o que significam DEF e EXC.
2. Em Santa Helena, alguma classificação mudou entre 1990 e 2020? Qual foi a mais sensível?
3. Nas 27 capitais, qual classificação detectou mais mudanças? Por que você acha que isso acontece?
4. Liste as capitais em que pelo menos 3 classificações indicam mudança.
5. Holdridge costuma mudar pouco. Explique por quê, pensando na escala logarítmica das suas faixas.

---

## ✅ Checklist do Capítulo 9

- [ ] Entendi ETP, balanço hídrico, DEF, EXC e biotemperatura
- [ ] Classifiquei Santa Helena pelas quatro classificações
- [ ] Comparei a sensibilidade das classificações nas 27 capitais
- [ ] Salvei `comparacao_classificacoes_27.csv`
- [ ] Respondi os exercícios
- [ ] ✅ **Ponto de controle:** apresentei os resultados dos Capítulos 7, 8 e 9 ao orientador antes de iniciar a Fase B

**Entregável 9:** notebook `cap09_outras_classificacoes.ipynb` + `comparacao_classificacoes_27.csv` + tabela de concordância + apresentação curta da Fase A ao orientador.
