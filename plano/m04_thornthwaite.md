# Missão 4: Classificação de Thornthwaite e as suas folgas

> **Pergunta da missão:** qual a classe de Thornthwaite de Santa Helena, e o quão perto ela está de mudar?
> **Duração:** 3 semanas
> **Notebook:** `m04_thornthwaite.ipynb`
> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com)
> 📓 **Notebook de exemplo:** [Exemplo 05: Thornthwaite e folgas (abrir no Colab)](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/05_thornthwaite_folgas.ipynb). O exemplo é feito para Santa Helena (e Curitiba); na seção ✍️ **Sua vez**, você repete para as capitais.
> **Fim da fase 1:** nesta missão você prepara uma mini apresentação (5 slides)

---

## Por que isso importa

O Thornthwaite classifica o clima pela **água** (o balanço hídrico da Missão 3) e pela **energia** (a ETP).
A classe tem 4 partes, por exemplo **B3rB'4a'**:

| Parte | Exemplo | O que diz | Vem de |
|---|---|---|---|
| 1ª: umidade | **B3** (úmido) | se o clima é úmido ou seco | índice de umidade **Im** |
| 2ª: subtipo | **r** | se há pouca ou muita falta (ou sobra) de água | índices **Ia** e **Ih** |
| 3ª: térmica | **B'4** (mesotérmico) | quanta energia o clima tem | **ETP anual** |
| 4ª: concentração | **a'** | se a ETP se concentra no verão | **% da ETP no verão** |

Os índices, em %, são:
- **Ih** (índice hídrico) = 100 × EXC / ETP;
- **Ia** (índice de aridez) = 100 × DEF / ETP;
- **Im** (índice de umidade) = Ih − 0,6 × Ia.

## O que você vai aprender de Python

- ler um **dicionário** com vários valores (o resultado da função).

---

## Semana 1: a tabela de limites

Leia a seção sobre Thornthwaite de Aparecido et al. (2016) e **monte à mão** duas tabelas no notebook,
numa célula de texto:

1. **Umidade:** para cada faixa de Im, a letra (A, B4, B3, B2, B1, C2, C1, D, E).
2. **Térmica:** para cada faixa de ETP anual, a letra (A', B'4, B'3, B'2, B'1, C'2, C'1, D', E').

> 💡 Confira com o orientador: a biblioteca usa os limites de Im **−40, −20, 0, 20, 40, 60, 80, 100** e os de
> ETP **142, 285, 427, 570, 712, 855, 997, 1140 mm**. O artigo traz **885 mm** num dos limites; a
> biblioteca usa **855**, que é o valor do trabalho original de Thornthwaite (1948). Descubra qual é e
> anote no diário. É um bom exemplo de que **artigos também têm erros**.

---

## Semana 2: classificar

```python
!pip install agrometeorologiapy
import agrometeorologiapy as amp
import pandas as pd

# Dados de Santa Helena
latitude = -24.86
temperatura = [___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___]
chuva = [___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___]

# 1) ETP de Thornthwaite (como na Missão 3)
tabela = pd.DataFrame({'T_media_C': temperatura})
tabela = amp.thornthwaite_mensal(tabela, lat=latitude)
etp = tabela['ETP_mm_mes']

# 2) Classificação de Thornthwaite.
#    A função faz o balanço hídrico por dentro, com CAD = 100 mm.
resultado = amp.classificacao_thornthwaite(chuva, etp, latitude, CAD=100)

# 3) Mostra tudo o que a função devolveu
resultado
```

O resultado é um dicionário com vários valores. Pegue os mais importantes, **um por linha**:

```python
classe = resultado['classe']
descricao = resultado['descricao']
indice_umidade = resultado['Im']
indice_hidrico = resultado['Ih']
indice_aridez = resultado['Ia']
etp_anual = resultado['ETP_anual']

print('Classe:', classe, '-', descricao)
print('Im (%):', round(indice_umidade, 1))
print('Ih (%):', round(indice_hidrico, 1))
print('Ia (%):', round(indice_aridez, 1))
print('ETP anual (mm):', round(etp_anual))
```

> 🧠 Confira: a ETP anual e o excedente são iguais aos que você calculou na Missão 3?

---

## Semana 3: as folgas de Thornthwaite

Agora é o mesmo raciocínio da Missão 2. Olhe a sua tabela de limites e encontre, **à mão**, os dois limites
entre os quais o Im de Santa Helena está. Por exemplo, se Im = 72,4, ele está entre **60** e **80** (classe
B3).

```python
# Digite os dois limites da faixa em que o Im de Santa Helena está
limite_de_baixo_im = ___
limite_de_cima_im = ___

# Quanto o Im precisaria CAIR para mudar de classe (ficar mais seco)
folga_im_para_baixo = indice_umidade - limite_de_baixo_im

# Quanto o Im precisaria SUBIR para mudar de classe (ficar mais úmido)
folga_im_para_cima = limite_de_cima_im - indice_umidade

print('Im pode cair', round(folga_im_para_baixo, 1), 'pontos antes de mudar de classe')
print('Im pode subir', round(folga_im_para_cima, 1), 'pontos antes de mudar de classe')
```

Faça o mesmo para a **ETP anual** com os limites térmicos:

```python
limite_de_baixo_etp = ___
limite_de_cima_etp = ___

folga_etp_para_baixo = etp_anual - limite_de_baixo_etp
folga_etp_para_cima = limite_de_cima_etp - etp_anual

print('ETP anual pode cair', round(folga_etp_para_baixo), 'mm antes de mudar a letra térmica')
print('ETP anual pode subir', round(folga_etp_para_cima), 'mm antes de mudar a letra térmica')
```

> 💭 Na Missão 9 você vai escrever uma função que encontra esses limites **sozinha**. Por enquanto, fazer à
> mão ajuda a entender o que a função vai fazer.

### Experimente

Some **1 °C** a todos os meses e refaça a classificação. O que muda primeiro: a letra de umidade ou a
térmica? Por quê? (Dica: lembre do experimento 2 da Missão 3.)

---

## 🎤 Mini apresentação: fim da fase 1

Prepare **5 slides** para o encontro (Google Slides serve):

1. Onde fica Santa Helena e o climograma (M0)
2. A classe de Köppen e o que cada letra significa (M1)
3. As folgas de Köppen: qual critério está mais perto de mudar (M2)
4. O balanço hídrico (M3)
5. A classe de Thornthwaite e as suas folgas (M4)

Fale por **5 a 7 minutos**. É um treino para o evento científico do fim do projeto.

## 📦 Entregável

- ✍️ A seção **Sua vez** do notebook de exemplo, feita para as capitais pedidas.
- O notebook com a classificação e as folgas de Thornthwaite.
- A tabela de limites (célula de texto).
- Os 5 slides.

## 🗣️ Para o próximo encontro, saiba responder

- O que significa cada uma das 4 partes da classe de Santa Helena?
- O que é o Im e como ele é calculado?
- Em Santa Helena, qual está mais perto de mudar: um critério de Köppen ou um de Thornthwaite?

## ✅ Checklist

- [ ] Montei as tabelas de limites de Im e de ETP
- [ ] Classifiquei com a biblioteca
- [ ] Calculei as folgas de Im e de ETP
- [ ] Fiz o experimento de +1 °C
- [ ] Preparei os 5 slides
- [ ] Preenchi o diário de bordo
