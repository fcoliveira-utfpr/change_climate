# Fase 3: Muitos lugares (missões 11 a 16)

> 📁 **Pasta do projeto:** [abrir no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) · 🚀 [abrir o Google Colab](https://colab.research.google.com)

> **Para o orientador:** as M11 a M16 são **fichas**, não missões detalhadas. Detalhe cada uma no ciclo
> anterior, no mesmo formato das missões 0 a 10, quando já souber o ritmo da aluna. Se o calendário apertar, corte na
> ordem: M13 (mapas com contorno) → M12 (27 capitais) → M14 (comparação Köppen × Thornthwaite). M11, M15 e
> M16 não devem ser cortadas.

**Pergunta da fase:** onde no Brasil os critérios de Köppen e de Thornthwaite estão mais perto de cruzar o
limiar, e em que ritmo?

---

> 💡 Quando a fase 3 começa, a aluna já tem as séries das 27 capitais (extraídas por ela na M5), o resumo
> das 27 (M9) e o ritmo das 27 (M10). A fase 3 aprofunda, compara e comunica esses resultados.

## M11: Cinco climas na beirada

- **Pergunta:** que lugares do Brasil estão perto de um limiar, e de qual?
- **Python novo:** `for` sobre uma **lista de cidades**; juntar várias tabelas numa só.
- **Pontos sugeridos** (cada um perto de um limiar diferente; confirme com os dados):
  Brasília (Aw × Cwa: mês mais frio perto de 18 °C), Curitiba (Cfb × Cfa: mês mais quente perto de 22 °C),
  Manaus (Af × Am: mês mais seco perto de 60 mm), uma cidade do semiárido (BSh × As/Aw: limiar de aridez) e
  Santa Helena.
- **Entregável:** uma tabela-resumo com uma linha por cidade (classe em 1990 e 2025, folga do critério
  crítico em 1990 e 2025, ritmo e anos até cruzar) e uma figura com as folgas no tempo, uma linha por
  cidade.

## M12: As 27 capitais por região

- **Pergunta:** quantas capitais mudaram de classe entre 1990 e 2025? Em quantas a folga diminuiu? Há
  diferença entre as regiões?
- **Python novo:** juntar duas tabelas (`merge`: o resumo da M9 com o ritmo da M10) e agrupar por região
  (`groupby`).
- **Entregável:** `resultados/resumo_por_regiao.csv` e um parágrafo por região.
- **Lembrar:** 27 pontos representam as **capitais**, não os estados inteiros.

## M13: Mapas dos pontos

- **Pergunta:** existe um padrão geográfico nas folgas e nos ritmos?
- **Python novo:** gráfico de dispersão longitude × latitude colorido por valor; contorno dos estados com
  `geobr`.
- **Entregável:** dois mapas: a folga do critério mais próximo em 2025 e o ritmo (com destaque nos pontos
  com p < 0,05).

## M14: Köppen × Thornthwaite, qual reage mais?

- **Pergunta:** a mesma mudança de clima aproxima mais um limiar de Köppen ou um de Thornthwaite?
- **Python novo:** nenhum (é uma missão de **análise e escrita**, para dar um respiro na programação).
- **Entregável:** uma tabela com, para cada capital, o critério mais próximo de cada classificação e as duas
  folgas, e uma página de discussão. Conectar com a Missão 3: o aquecimento aumenta a ETP e reduz o Im,
  mesmo sem mudança na chuva.

## M15: Resumo e pôster para evento

- **Pergunta:** como contar a pesquisa em 300 palavras?
- **Entregável:** o resumo para o SICITE (ou outro evento) com: objetivo (1 frase), métodos (2 a 3 frases),
  2 ou 3 resultados **com números** e conclusão (1 frase). Depois, o pôster.

## M16: Relatório final e organização do código

- **Entregável:** o relatório final (estrutura da M10, ampliada com a fase 3) e os notebooks organizados num
  repositório no GitHub:

```
mudanca_climatica_br/
├── README.md        → objetivo, dados, como reproduzir
├── notebooks/       → m00 a m14, limpos e comentados
├── resultados/      → tabelas finais (CSV)
└── figuras/         → figuras finais
```

- Antes de publicar: rodar cada notebook do início ao fim e apagar as células de teste.

---

## Depois da IC (renovação ou TCC)

Para uma continuação, o mesmo método vai para a **grade completa** do Xavier (cada pixel de ~10 km), com as
versões `_grade` das funções da biblioteca (`classificacao_koppen_grade`,
`classificacao_thornthwaite_grade`). O resultado são mapas de folga e de ritmo do Brasil inteiro. O
processamento é pesado, então só faz sentido quando as funções da M9 estiverem dominadas.
