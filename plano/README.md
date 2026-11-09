# Plano de execução — guia do orientador

**Projeto:** O clima está perto de mudar de classe? Köppen e Thornthwaite com o clima de referência móvel
**Formato:** iniciação científica de ~12 meses, encontros a cada 3 semanas, aluna sem experiência em programação

📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [Google Colab](https://colab.research.google.com) · 📚 [agrometeorologiapy](https://github.com/fcoliveira-utfpr/agrometeorologiapy)

---

## 1. A ideia em uma frase

A aluna aprende a programar **fazendo a pesquisa**: cada ciclo de 3 semanas tem **uma pergunta científica
pequena**, **um código curto** que a responde e **um resultado visível** (uma figura ou uma tabela) que ela
apresenta no encontro.

## 2. A pergunta da pesquisa

> Mesmo quando a classe climática **não muda**, o clima pode estar **se aproximando** de mudar.
> Quanto falta para cada critério de Köppen e de Thornthwaite cruzar o seu limiar? Em que ritmo?

Para isso, em vez de registrar só a classe, medimos a **folga** de cada critério, ou seja, a distância até o
limiar:

| Classificação | Critério | Folga |
|---|---|---|
| Köppen | A × C | T do mês mais frio − 18 °C |
| Köppen | a × b | T do mês mais quente − 22 °C |
| Köppen | Af × Am/Aw | chuva do mês mais seco − 60 mm |
| Köppen | Am × Aw | chuva do mês mais seco − (100 − chuva anual / 25) |
| Köppen | B × não B | chuva anual − limiar de aridez, 10 × (2T + 14), ajustado pela chuva de verão |
| Thornthwaite | umidade | distância do Im ao limite de classe mais próximo (−40, −20, 0, 20, 40, 60, 80, 100) |
| Thornthwaite | térmica | distância da ETP anual ao limite mais próximo (142, 285, 427, 570, 712, 855, 997, 1140 mm) |

São os mesmos limiares que a `agrometeorologiapy` (v1.0.1) usa em `classificacao_koppen` e
`classificacao_thornthwaite`. Assim, a folga calculada pela aluna é coerente com a classe que a biblioteca
devolve.

## 3. Princípios do plano

1. **Pesquisa desde o primeiro dia.** Não existe "módulo de Python" separado. Cada conceito de programação
   aparece quando a pesquisa precisa dele.
2. **Um conceito novo de Python por missão.** Em cada missão há uma lista curta, "o que você vai aprender de
   Python", com no máximo 2 ou 3 itens.
3. **Código simples e comentado, mesmo que fique mais longo.** Uma operação por linha, nomes de variáveis em
   português e por extenso (`t_mes_frio`, e não `tf`), um comentário antes de cada passo, sem atalhos
   compactos (sem list comprehension, sem encadear muitos métodos).
4. **Digitar, não copiar (fase 1).** Nas missões 1 a 4, ela digita o código. É lento de propósito: é assim
   que se aprende a sintaxe. A partir da missão 5, pode copiar os modelos, mas tem de completar as lacunas
   (`___`).
5. **Resultado visível em toda missão.** Toda missão termina numa figura ou tabela que ela entende e consegue
   explicar.
6. **Ela explica, você pergunta.** No encontro, quem fala primeiro é a aluna.
7. **Você não mexe no código dela.** Você dá pistas (seção 7), mas quem escreve é ela.
8. **Erro faz parte do trabalho.** Todo erro vai para o diário de bordo, com o que ela tentou e como
   resolveu.

## 4. O ciclo de 3 semanas

| Semana | O que a aluna faz | Tempo sugerido |
|---|---|---|
| 1 | lê a missão e a leitura indicada; roda a primeira parte do código | 2–4 h |
| 2 | faz a parte principal; **envia o check-in** (uma figura ou tabela + uma dúvida) | 3–5 h |
| 3 | termina o entregável, escreve a interpretação, prepara a fala de 5 min | 2–4 h |

- **A carga cresce aos poucos.** Na fase 1, as missões são pequenas (~3 h/semana de prática). Na fase 3,
  chegam a ~8–10 h/semana. Como isso se encaixa na carga horária da bolsa é decisão sua.
- **Check-in na semana 2.** É uma mensagem curta: "fiz isto, travei aqui". Com encontros a cada 3 semanas,
  esse contato evita que ela passe 3 semanas travada.
- **Regra dos 30 minutos.** Se ficar travada mais de 30 minutos no mesmo erro, ela manda um print do erro
  com o que já tentou. Você responde com uma pista, não com a solução.
- **Uma missão pode durar dois ciclos, sem culpa.** O ritmo é o dela. Se o calendário apertar, corte a
  fase 3 (seção 9), nunca as missões da fase 1.

## 5. Roteiro de cada encontro (50–60 min)

1. **Ela apresenta (10 min).** Mostra o entregável e explica o resultado com as próprias palavras.
2. **Você pergunta (15 min).** Use três tipos de pergunta:
   - *O quê:* "o que significa esse número negativo?"
   - *Por quê:* "por que você usou `min` aqui?"
   - *E se:* "e se a chuva de julho dobrasse, a classe mudaria?"
   Peça também para ela explicar **duas linhas do código escolhidas por você**.
3. **Diário de bordo (10 min).** Dúvidas e erros do ciclo.
4. **Próxima missão (15 min).** Você apresenta a pergunta e **demonstra ao vivo só o conceito novo** (por
   exemplo, um `for` com 3 anos). Ela sai sabendo o que fazer na semana 1.
5. **Combinados (5 min).** Data do check-in e do próximo encontro.

## 6. Diário de bordo

Cada notebook termina com três células de texto, preenchidas pela aluna:

- **O que aprendi** (2–3 frases);
- **Erros que encontrei e como resolvi** (copiar a última linha da mensagem de erro);
- **Dúvidas** (para o encontro).

O diário é o que você mais deve ler. Ele mostra se ela está entendendo ou só fazendo rodar.

## 7. Como ajudar sem fazer por ela: pistas em 3 níveis

1. **Pergunta:** "O que a mensagem de erro diz na última linha?"
2. **Onde olhar:** "Compare a linha 4 com o exemplo da seção 3 da missão."
3. **Exemplo análogo:** mostre o mesmo conceito com **outros dados** (outra cidade, outra variável), nunca a
   linha pronta da missão dela.

## 8. Uso de IA (Gemini no Colab, ChatGPT etc.)

Sugestão de regra para combinar no encontro 0:

- **Pode** pedir à IA para explicar uma mensagem de erro ou um conceito ("o que é um DataFrame?").
- **Não pode** pedir à IA para fazer a missão.
- **Toda linha entregue tem de ser explicável.** As "duas linhas escolhidas" do encontro são justamente o
  teste disso.
- Na fase 1, recomendo **desativar o autocompletar de código por IA** nas configurações do Colab. Ela tem de
  digitar e errar sozinha primeiro.

## 9. Calendário

| Fase | Ciclos | Missões | Pergunta da fase | Marco |
|---|---|---|---|---|
| **1. Um lugar, o clima em números** | 1–5 (meses 1–3) | M0–M4 | Qual o clima de Santa Helena e o quão perto ele está dos limiares? | mini apresentação (5 slides) |
| **2. Os dados e o tempo** | 6–11 (meses 4–8) | M5–M10 | De onde vêm os dados? A folga está diminuindo? Em que ritmo? | **relatório parcial** |
| **3. Muitos lugares** | 12–17 (meses 9–12) | M11–M16 | Onde no Brasil os critérios estão mais perto de cruzar? | resumo para evento + relatório final |

As missões M0 a M10 estão detalhadas, uma por arquivo. As M11 a M16 estão em
[m11_m16_fase3.md](m11_m16_fase3.md) como fichas; detalhe cada uma no ciclo anterior, quando já souber o
ritmo da aluna.

| Missão | Arquivo | Conceito de Python novo | 📓 Notebook de exemplo | ✍️ "Sua vez" |
|---|---|---|---|---|
| M0 | [m00_boas_vindas.md](m00_boas_vindas.md) | abrir o Colab, rodar uma célula | [01 Climograma](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/01_climograma.ipynb) | 3 capitais (normais do INMET) |
| M1 | [m01_numeros_do_clima.md](m01_numeros_do_clima.md) | variável, lista, `sum`, `min`, `max`, `print` | [02 Köppen](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/02_koppen_um_ponto.ipynb) | 5 capitais (INMET) |
| M2 | [m02_folga.md](m02_folga.md) | contas com variáveis, gráfico de barras | [03 Folgas de Köppen](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/03_folgas_koppen.ipynb) | 5 capitais (INMET) |
| M3 | [m03_balanco_hidrico.md](m03_balanco_hidrico.md) | tabela (`DataFrame`), coluna | [04 Balanço hídrico](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/04_balanco_hidrico.ipynb) | 5 capitais (INMET) |
| M4 | [m04_thornthwaite.md](m04_thornthwaite.md) | dicionário (ler o resultado da função) | [05 Thornthwaite](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/05_thornthwaite_folgas.ipynb) | 5 capitais (INMET) |
| M5 | [m05_gee.md](m05_gee.md) | criar o projeto no Earth Engine, extrair dados | [06 Extrair no GEE](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/06_extrair_dados_gee.ipynb) | **extrair as 27 capitais** |
| M6 | [m06_serie_historica.md](m06_serie_historica.md) | ler CSV, datas, média anual | [07 Série histórica](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/07_serie_historica.ipynb) | 5 capitais |
| M7 | [m07_duas_normais.md](m07_duas_normais.md) | recortar período, média por mês | [08 Duas normais](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/08_duas_normais.ipynb) | 10 capitais |
| M8 | [m08_janela_movel.md](m08_janela_movel.md) | repetição (`for`) | [09 Janela móvel](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/09_janela_movel.ipynb) | 5 capitais |
| M9 | [m09_funcoes.md](m09_funcoes.md) | criar a própria função (`def`), `if` | [10 Funções e capitais](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/10_funcoes_e_capitais.ipynb) | **27 capitais** + mapa |
| M10 | [m10_ritmo.md](m10_ritmo.md) | teste de tendência (biblioteca pronta) | [11 Tendência e ritmo](https://colab.research.google.com/github/fcoliveira-utfpr/change_climate/blob/main/code/notebooks_exemplo/11_tendencia_ritmo.ipynb) | **27 capitais** |

### Como os notebooks de exemplo funcionam

- Ficam em [`code/notebooks_exemplo/`](../code/notebooks_exemplo/) e abrem direto no Colab. A aluna só faz
  **Arquivo → Salvar uma cópia no Drive**.
- **O exemplo é feito para um lugar (Santa Helena, às vezes também Curitiba). Os outros ficam para ela**: a
  seção ✍️ **Sua vez** mostra como repetir e pede a replicação para as capitais.
- **De onde vêm os dados de cada um:**
  - exemplos 01–05: a normal de Santa Helena e de Curitiba já vem escrita no código. Na "Sua vez", ela
    procura as normais das capitais no portal do INMET
    ([Normais Climatológicas 1991–2020](https://portal.inmet.gov.br/normais)) e digita as listas;
  - exemplo 06 (M5): ela **extrai do Earth Engine**. O exemplo extrai Santa Helena; na "Sua vez", ela monta
    a tabela de coordenadas das 27 capitais e extrai todas para `dados/capitais/` no Drive dela;
  - exemplos 07–11: o exemplo lê Santa Helena e Curitiba do GitHub (link raw, em
    [`code/dados/`](../code/dados/)); a "Sua vez" lê as capitais que **ela mesma extraiu**, no Drive.
- Um bônus da M5: ela pode comparar a normal do Xavier (pixel) com a do INMET (estação) nas capitais que
  digitou na fase 1.

> ⚠️ **Os links do Colab e do GitHub só funcionam depois do `git push`** para
> `fcoliveira-utfpr/change_climate` (branch `main`).

## 10. O que você prepara

**Antes do encontro 0:**
- [ ] 📁 [pasta `mudanca_climatica_br/` no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing),
      compartilhada com a aluna **como editora** (ela precisa salvar notebooks e figuras). ✅ As subpastas
      `dados/`, `notebooks/`, `figuras/`, `resultados/` e `leituras/` já estão criadas;
- [ ] PDF de Alvares et al. (2013) e de Aparecido et al. (2016) em `leituras/`.

A normal 1991–2020 de Santa Helena (M0 a M4) já está escrita no código da M0.

**Dados de exemplo:** ✅ `santa_helena_mensal.csv` e `curitiba_mensal.csv` (Xavier v3.2.4, 1961–2025, colunas
`data`, `tmed` e `chuva`) estão no GitHub em [`code/dados/`](../code/dados/) e também em `dados/` no Drive. Os
dois foram gerados com [`code/extrair_xavier_pontos.py`](../code/extrair_xavier_pontos.py), o mesmo código que
ela vai usar na M5. Pontos: Santa Helena (−24,86; −54,33) e Curitiba (−25,43; −49,27). **Os dados das
capitais não são fornecidos: ela extrai na M5.**

**Antes da M5:** marcar a semana 1 da M5 **junto com ela** (criar e registrar o projeto no Earth Engine, uso
não comercial, Community Tier, gratuito e sem cartão).

## 11. Sinais de alerta e o que fazer

| Sinal | Provável causa | Ação |
|---|---|---|
| Não manda o check-in duas vezes | travou e tem vergonha de perguntar | mensagem curta e leve: "me manda o que tiver, mesmo com erro" |
| Diário vazio ou genérico | está só fazendo rodar | no encontro, peça para ela explicar 4 linhas em vez de 2 |
| Código perfeito, mas ela não explica | IA ou colega fizeram por ela | reforce a regra da seção 8; repita a missão com outra cidade |
| Entrega no prazo, mas exausta | missão grande demais | divida a próxima missão em dois ciclos |
| Faz além do pedido | está engajada | ofereça os "desafios opcionais" das missões |

## 12. Como avaliar cada missão

Três perguntas, cada uma com resposta sim, parcial ou não:

1. **Entregou** a figura ou tabela pedida, salva na pasta certa?
2. **Explica** o código (as duas linhas escolhidas por você)?
3. **Interpreta** o resultado (o que o número diz sobre o clima)?

Para avançar, basta ter "sim" na 1 e pelo menos "parcial" na 2 e na 3. O que faltar volta como ponto de
atenção na missão seguinte, sem repetir a missão.

## 13. O que esperar dos dados

Na preparação, rodei as missões com os dados reais do Xavier. Os notebooks de exemplo mostram estes
resultados para Santa Helena e Curitiba. Por isso, **a descoberta própria da aluna fica nas capitais**
(seção "Sua vez"). Se quiser que ela descubra também Santa Helena, peça que faça a missão **antes** de abrir
o notebook de exemplo.

| Ponto | O que acontece | Onde ela descobre |
|---|---|---|
| Santa Helena | **Cfa em 1961–1990, Af em 1991–2020.** O mês mais frio passa de 17,4 para 18,9 °C (folga A/C de −0,59 para +0,92 °C). Na janela móvel, a classe muda em 2000–2002 e não volta mais. No Thornthwaite, a letra térmica passa de B'4 para A' por volta de 1996. | M1 (diferença com o mapa de Alvares), M7, M8 |
| Curitiba | **Cfb até 1993; oscila (Cfa em 1994, Cfb em 1996); Cfa a partir de 1997.** Folga a/b de −0,08 °C em 1990 e +0,72 °C em 2025, com o mês mais quente aquecendo 0,3 °C por década (p < 0,05): um exemplo perfeito de "mudança pequena que muda a classe". No Thornthwaite, o Im também **oscila** em torno de 80 (B3 ↔ B4). | M9, M10 |

Dois cuidados para a discussão com ela:
- **É um pixel de 0,1° do Xavier, não uma estação.** A classe "Af" de Santa Helena e a "Cfa" de Curitiba
  podem diferir do Alvares et al. (2013) também pela fonte e pelo período dos dados. Essa comparação é um bom
  tema para o relatório parcial.
- **Na M10, as duas cidades caem no caso "acima do limiar e subindo"** (já cruzaram). Para o cálculo de "anos
  até cruzar" ficar interessante, a M11 traz cidades que ainda estão abaixo do limiar.

## 14. Leituras (ao longo do projeto)

- ALVARES, C. A. et al. Köppen's climate classification map for Brazil. *Meteorologische Zeitschrift*, v. 22,
  n. 6, p. 711–728, 2013. (M1, M2)
- APARECIDO, L. E. O. et al. Köppen, Thornthwaite and Camargo climate classifications for climatic zoning in
  the State of Paraná, Brazil. *Ciência e Agrotecnologia*, v. 40, n. 4, 2016. (M3, M4)
- PEREIRA, A. R.; ANGELOCCI, L. R.; SENTELHAS, P. C. *Agrometeorologia: fundamentos e aplicações práticas*.
  2002. Capítulos de balanço hídrico e classificação climática. (M3, M4)
- XAVIER, A. C. et al. New improved Brazilian daily weather gridded data (1961–2020). *International Journal
  of Climatology*, 2022. (M6)
- THORNTHWAITE, C. W. An approach toward a rational classification of climate. *Geographical Review*, v. 38,
  n. 1, 1948. (opcional, M4)

> Confira cada referência na fonte original antes de usá-la no relatório.
