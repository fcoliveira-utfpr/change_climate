# Missão 2: A folga, ou quanto falta para mudar

> **Pergunta da missão:** quanto falta para cada critério de Köppen mudar em Santa Helena?
> **Duração:** 3 semanas
> **Notebook:** `m02_folga_koppen.ipynb`
> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com)
> 📓 **Notebook de exemplo:** [Exemplo 03: Folgas de Köppen (abrir no Colab)](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/03_folgas_koppen.ipynb). O exemplo é feito para Santa Helena (e Curitiba); na seção ✍️ **Sua vez**, você repete para as capitais.

---

## Por que isso importa

Na Missão 1, a classe foi o resultado. Mas a classe é só um **rótulo**: ela não diz se o clima está "no meio"
da classe ou "na beirada". Nesta missão você vai medir essa distância, a **folga**, para cada critério.

**Folga = valor do clima − limiar da regra**

- **Folga positiva:** o valor está **acima** do limiar.
- **Folga negativa:** o valor está **abaixo** do limiar.
- **Folga perto de zero:** o critério está **perto de mudar**.

Exemplo: se o mês mais frio tem 16,6 °C, a folga A/C é 16,6 − 18 = **−1,4 °C**. O clima é C (temperado) e
precisaria esquentar 1,4 °C no mês mais frio para virar A (tropical).

## O que você vai aprender de Python

- fazer **contas com variáveis**;
- fazer um **gráfico de barras** com uma linha no zero.

---

## Semana 1: as folgas de Köppen

No notebook novo, digite de novo as listas da Missão 1. Repetir faz parte do aprendizado.

```python
# Latitude e normal 1991-2020 de Santa Helena (os mesmos valores da Missão 1)
latitude = -24.86
temperatura = [___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___]
chuva = [___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___]

# Os números do clima (iguais aos da Missão 1)
chuva_anual = sum(chuva)
t_mes_frio = min(temperatura)
t_mes_quente = max(temperatura)
p_mes_seco = min(chuva)
```

Agora as folgas. **Cada uma corresponde a uma regra da tabela da Missão 1.**

```python
# Folga A/C: o mês mais frio comparado com 18 °C
#   positiva -> tropical (A); negativa -> temperado (C)
folga_A = t_mes_frio - 18

# Folga a/b: o mês mais quente comparado com 22 °C
#   positiva -> verão quente (a); negativa -> verão ameno (b)
folga_a = t_mes_quente - 22

# Folga Af: o mês mais seco comparado com 60 mm
#   positiva -> chove bem o ano todo (no grupo A, isso é Af)
folga_f = p_mes_seco - 60

# Folga Am: o mês mais seco comparado com o limiar da monção
#   o limiar depende da chuva anual: 100 - chuva_anual / 25
#   (nos nomes de variáveis, evite acentos e ç: escreva "moncao")
limiar_moncao = 100 - chuva_anual / 25
folga_m = p_mes_seco - limiar_moncao

# Mostra as folgas, arredondadas
print('Folga A/C (°C):', round(folga_A, 2))
print('Folga a/b (°C):', round(folga_a, 2))
print('Folga Af (mm):', round(folga_f, 1))
print('Folga Am (mm):', round(folga_m, 1))
```

> 🧠 **Interprete cada número antes de seguir.** Escreva uma frase para cada um, por exemplo: "A folga A/C é
> −1,4 °C: o mês mais frio precisaria esquentar 1,4 °C para o clima virar tropical."

> 💡 As folgas Af e Am só **decidem** a classe quando o clima é A. Se o clima for C, elas mostram o quanto a
> chuva do mês mais seco está longe desses limiares, caso ele um dia vire A.

---

## Semana 2: o gráfico das folgas

Temperatura (°C) e chuva (mm) têm unidades diferentes, então fazemos **dois gráficos**, lado a lado.

```python
import matplotlib.pyplot as plt

# Cria uma figura com 2 gráficos lado a lado (1 linha, 2 colunas)
fig, eixos = plt.subplots(1, 2, figsize=(10, 4))

# ----- Gráfico 1: folgas de temperatura -----
# eixos[0] é o gráfico da esquerda
nomes_temperatura = ['A/C (mês frio)', 'a/b (mês quente)']
folgas_temperatura = [folga_A, folga_a]
eixos[0].bar(nomes_temperatura, folgas_temperatura, color='tomato')

# Linha preta no zero: é o limiar. Barras perto dela = perto de mudar.
eixos[0].axhline(0, color='black')
eixos[0].set_ylabel('Folga (°C)')
eixos[0].set_title('Critérios de temperatura')

# ----- Gráfico 2: folgas de chuva -----
# eixos[1] é o gráfico da direita
nomes_chuva = ['Af (60 mm)', 'Am (monção)']
folgas_chuva = [folga_f, folga_m]
eixos[1].bar(nomes_chuva, folgas_chuva, color='steelblue')
eixos[1].axhline(0, color='black')
eixos[1].set_ylabel('Folga (mm)')
eixos[1].set_title('Critérios de chuva')

# Título geral da figura
fig.suptitle('Quanto falta para mudar? Santa Helena-PR, 1991-2020')

# Ajusta os espaços para nada ficar sobreposto
plt.tight_layout()
plt.show()
```

Salve a figura em `figuras/folgas_koppen_santa_helena.png`, como na Missão 0.

---

## Semana 3: comparar folgas de unidades diferentes

Uma folga de 1 °C é "muito" ou "pouco"? Depende de **quanto essa variável costuma mudar**. Converse sobre
isso no encontro. Por enquanto, faça uma conta simples:

```python
# Uma forma simples de comparar: a folga em % do próprio limiar
folga_A_pct = 100 * folga_A / 18
folga_f_pct = 100 * folga_f / 60

print('Folga A/C em % do limiar:', round(folga_A_pct, 1))
print('Folga Af em % do limiar:', round(folga_f_pct, 1))
```

> 💭 Isso é só uma primeira ideia. Na Missão 10 você vai medir o **ritmo** com que cada variável muda, uma
> forma muito melhor de saber se a folga é grande ou pequena.

### Desafio opcional: a folga do grupo B (seco)

O limiar de aridez depende da temperatura média anual (T) e de **quando** chove:

| Situação | Limiar (mm) |
|---|---|
| 70% ou mais da chuva no verão (out–mar) | 10 × (2T + 28) |
| 70% ou mais da chuva no inverno (abr–set) | 10 × (2T) |
| nos outros casos | 10 × (2T + 14) |

Calcule à mão a fração da chuva que cai no verão em Santa Helena e a folga B (chuva anual − limiar). Você
vai programar isso na Missão 7.

---

## 📦 Entregável

- ✍️ A seção **Sua vez** do notebook de exemplo, feita para as capitais pedidas.
- A figura `folgas_koppen_santa_helena.png`.
- Uma célula de texto com:
  1. uma frase para cada folga;
  2. **qual critério está mais perto de mudar** em Santa Helena, e para qual classe ele levaria.

## 🗣️ Para o próximo encontro, saiba responder

- O que significa uma folga negativa?
- Por que fizemos dois gráficos em vez de um?
- Se o mês mais frio esquentasse 0,5 °C, a folga A/C ficaria quanto?

## ✅ Checklist

- [ ] Calculei as 4 folgas e escrevi uma frase para cada
- [ ] Fiz e salvei o gráfico das folgas
- [ ] Fiz a conta da folga em %
- [ ] Preenchi o diário de bordo
