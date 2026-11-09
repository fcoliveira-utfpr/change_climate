# Missão 1: Os números do clima e a primeira classificação

> **Pergunta da missão:** qual é a classe de Köppen de Santa Helena, e por quê?
> **Duração:** 3 semanas
> **Notebook:** `m01_koppen_santa_helena.ipynb`
> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com)
> 📓 **Notebook de exemplo:** [Exemplo 02: Köppen (abrir no Colab)](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/02_koppen_um_ponto.ipynb). O exemplo é feito para Santa Helena (e Curitiba); na seção ✍️ **Sua vez**, você repete para as capitais.

---

## Por que isso importa

Para saber se um clima está "perto de mudar", primeiro precisamos entender **como ele é classificado**.
Nesta missão você vai classificar Santa Helena **duas vezes**: primeiro **à mão** (com papel e caneta) e
depois **com o computador**. Se as duas derem o mesmo resultado, você entendeu a regra.

## O que você vai aprender de Python

- **variável:** um nome que guarda um valor (`chuva_anual = 1820`);
- **lista:** vários valores em sequência (`[25.5, 25.3, ...]`) e as funções `sum`, `min` e `max`;
- **usar uma biblioteca:** chamar uma função pronta, que alguém já escreveu.

> ✍️ **Nesta missão, digite o código, não copie e cole.** É mais lento, mas é assim que os dedos e a cabeça
> aprendem. Os erros de digitação também ensinam.

---

## Semana 1: Köppen no papel

### 1. Leia as regras

Leia a seção de metodologia de Alvares et al. (2013). As regras de Köppen, de forma simplificada:

| Passo | Pergunta | Se sim | Se não |
|---|---|---|---|
| 1 | A chuva anual é menor que o limiar de aridez? | grupo **B** (seco) | vá ao passo 2 |
| 2 | O mês mais frio tem média **≥ 18 °C**? | grupo **A** (tropical) | grupo **C** (temperado) |
| 3A | (se A) o mês mais seco tem **≥ 60 mm**? | **Af** | Am, Aw ou As |
| 3C | (se C) existe estação seca? no inverno, **w**; no verão, **s** | Cw ou Cs | **Cf** |
| 4C | (se C) o mês mais quente tem média **≥ 22 °C**? | 3ª letra **a** | 3ª letra **b** |

> No Hemisfério Sul, o **verão** vai de outubro a março e o **inverno** de abril a setembro.

### 2. Classifique Santa Helena à mão

Com os valores da normal 1991–2020 de Santa Helena (os mesmos do código da Missão 0), descubra, **no
papel**:

1. a temperatura do mês mais frio;
2. a temperatura do mês mais quente;
3. a chuva do mês mais seco;
4. a chuva anual (some os 12 meses).

Agora siga a tabela de regras e escreva a classe. Tire uma foto da folha e guarde em `figuras/`.

---

## Semana 2: os mesmos números com Python

Crie o notebook `m01_koppen_santa_helena` e **digite** cada bloco numa célula separada.

### 3. Variáveis e listas

```python
# Uma variável guarda um valor. O sinal = significa "guarde isto neste nome".
latitude = -24.86       # latitude de Santa Helena (negativa = Hemisfério Sul)

# Uma lista guarda vários valores, entre colchetes, separados por vírgula.
# Digite aqui os 12 valores de Santa Helena (janeiro a dezembro), os mesmos da Missão 0.
temperatura = [___, ___, ___, ___, ___, ___,
               ___, ___, ___, ___, ___, ___]

chuva = [___, ___, ___, ___, ___, ___,
         ___, ___, ___, ___, ___, ___]

# print mostra um valor na tela
print(temperatura)
print(chuva)
```

> ⚠️ No Python, o separador decimal é o **ponto**: escreva `25.5`, não `25,5`.

### 4. Os números do clima

```python
# Chuva anual: soma dos 12 meses
chuva_anual = sum(chuva)

# Temperatura média anual: soma dos 12 meses dividida por 12
temperatura_media_anual = sum(temperatura) / 12

# Temperatura do mês mais frio: o menor valor da lista
t_mes_frio = min(temperatura)

# Temperatura do mês mais quente: o maior valor da lista
t_mes_quente = max(temperatura)

# Chuva do mês mais seco: o menor valor da lista de chuva
p_mes_seco = min(chuva)

# Mostra os resultados. round(valor, 1) arredonda para 1 casa decimal.
print('Chuva anual (mm):', chuva_anual)
print('Temperatura média anual (°C):', round(temperatura_media_anual, 1))
print('Mês mais frio (°C):', t_mes_frio)
print('Mês mais quente (°C):', t_mes_quente)
print('Mês mais seco (mm):', p_mes_seco)
```

> 🧠 **Antes de rodar, preveja:** escreva no caderno o valor que você espera em cada linha, usando a sua
> conta da semana 1. Depois rode e compare.

---

## Semana 3: deixar o computador classificar

### 5. Instalar e usar a biblioteca

Uma **biblioteca** é um conjunto de funções que alguém já escreveu e testou. A `agrometeorologiapy` foi
escrita pelo seu orientador e já sabe classificar o clima.

```python
# Instala a biblioteca no Colab (só precisa rodar uma vez por sessão)
!pip install agrometeorologiapy
```

```python
# Carrega a biblioteca e dá a ela o apelido "amp"
import agrometeorologiapy as amp

# Pede à biblioteca a classificação de Köppen.
# Ela precisa de: as 12 temperaturas, as 12 chuvas e a latitude.
resultado = amp.classificacao_koppen(temperatura, chuva, latitude)

# Mostra o resultado completo
print(resultado)
```

O resultado vem assim: `{'id': 9, 'classe': 'Cfa'}`. Isso é um **dicionário**: cada valor tem um nome
(`'id'` e `'classe'`). Para pegar só a classe:

```python
# Pega só o valor guardado com o nome 'classe'
classe = resultado['classe']
print('Classe de Köppen de Santa Helena:', classe)
```

### 6. Experimente

Mude **um** número da lista por vez, rode tudo de novo e veja se a classe muda. Antes de cada mudança,
**preveja** o que vai acontecer.

1. Diminua **2 °C** só no mês mais frio. A classe muda? Qual letra mudou, e por quê?
2. Volte ao valor original e coloque **20 mm** na chuva do mês mais seco. A classe muda?
3. **Desafio:** qual a **menor** mudança na temperatura do mês mais frio que faz a classe mudar? E na do mês
   mais quente?

> 🧠 Esse desafio é, em miniatura, a pergunta da pesquisa inteira.

### 7. Compare com a literatura

Procure Santa Helena (oeste do Paraná) no mapa de Alvares et al. (2013). A classe que você encontrou é a
mesma do mapa? Se **não** for, não se preocupe: anote no diário e leve ao encontro. Pense em duas razões que
poderiam explicar a diferença. (Dica: de que período são os dados do mapa? E os seus?)

---

## Se der erro

| Mensagem (última linha) | O que costuma ser |
|---|---|
| `SyntaxError: invalid syntax` | faltou vírgula entre números, ou usou vírgula como decimal |
| `NameError: name 'temperatura' is not defined` | a célula que cria `temperatura` não foi rodada |
| `ModuleNotFoundError: No module named 'agrometeorologiapy'` | faltou rodar o `!pip install` |

## 📦 Entregável

- ✍️ A seção **Sua vez** do notebook de exemplo, feita para as capitais pedidas.
- O notebook com os blocos 3 a 6 funcionando.
- Uma célula de texto com:
  1. a classe obtida **à mão** e a obtida **pela biblioteca** (são iguais?);
  2. o significado de **cada letra** da classe de Santa Helena;
  3. as respostas do item 6;
  4. a comparação com o mapa de Alvares et al. (2013), item 7.
- A foto da classificação à mão.
- O diário de bordo.

## 🗣️ Para o próximo encontro, saiba responder

- Qual a diferença entre `sum(chuva)` e `min(chuva)`?
- Por que o resultado da biblioteca vem com `{ }` e o que significa `resultado['classe']`?
- Qual critério de Köppen você acha que está **mais perto** de mudar em Santa Helena?

## ✅ Checklist

- [ ] Classifiquei Santa Helena à mão
- [ ] Digitei e rodei os blocos 3 e 4
- [ ] Classifiquei com a biblioteca e comparei
- [ ] Fiz os experimentos do item 6
- [ ] Preenchi o diário de bordo
