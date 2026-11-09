# change_climate

**O clima está perto de mudar de classe?** Köppen e Thornthwaite calculados com um clima de referência móvel
(janelas de 30 anos, 1990–2025) para as capitais brasileiras.

A pesquisa não olha só a classe climática. Ela mede a **folga** de cada critério, isto é, quanto falta para o
critério cruzar o seu limiar e em que ritmo essa distância muda. Assim aparece o clima que ainda não mudou de
classe, mas está chegando perto.

📁 [Pasta no Google Drive](https://drive.google.com/drive/folders/1a53g-mdQavSETaSMqlC8Pr3xCWYX5WkY?usp=sharing) ·
🚀 [Google Colab](https://colab.research.google.com) ·
📚 [agrometeorologiapy](https://github.com/fcoliveira-utfpr/agrometeorologiapy)

## Por onde começar

| Para quem | Abra |
|---|---|
| Aluna | [Missão 0: boas-vindas](plano/m00_boas_vindas.md) e depois as missões, uma a cada encontro |
| Orientador | [Guia do orientador](plano/README.md): calendário, roteiro dos encontros, sistema de dicas |
| Quem quer rodar os exemplos | [Notebooks de exemplo](code/notebooks_exemplo/README.md), que abrem direto no Colab |

## O que tem aqui

```
plano/                      guia do orientador e as missões (m00 … m10, m11_m16_fase3)
code/notebooks_exemplo/     11 notebooks, um por missão, com Santa Helena e Curitiba
code/dados/                 séries mensais de exemplo (1961–2025), lidas pelos notebooks por link raw
code/extrair_xavier_pontos.py   script de extração dos dados no Google Earth Engine
```

Os exemplos usam só **Santa Helena (PR)** e **Curitiba (PR)**. No fim de cada notebook, a seção ✍️ **Sua vez**
pede para repetir o método para as capitais. Os dados das capitais não estão no repositório: a aluna os extrai
do Earth Engine na [Missão 5](plano/m05_gee.md) (notebook 06).

## Dados

- **Clima diário:** BR-DWGD (Xavier et al.), grade de 0,1°, 1961–2025, no Google Earth Engine
  (`projects/ee-alexandrexavier/assets/BR-DWGD`). A temperatura média é (Tmax + Tmin) / 2; a chuva mensal é a
  soma dos dias, e meses com algum dia faltando ficam vazios.
- **Normais de estação:** [INMET, Normais Climatológicas 1991–2020](https://portal.inmet.gov.br/normais), usadas
  nas missões 0 a 4.

Arquivos de exemplo (colunas `data`, `tmed`, `chuva`):

- [santa_helena_mensal.csv](https://raw.githubusercontent.com/fcoliveira-utfpr/change_climate/main/code/dados/santa_helena_mensal.csv) (−24,86; −54,33)
- [curitiba_mensal.csv](https://raw.githubusercontent.com/fcoliveira-utfpr/change_climate/main/code/dados/curitiba_mensal.csv) (−25,43; −49,27)

## Ferramentas

Python no Google Colab, com `pandas`, `matplotlib`, `earthengine-api`, `pymannkendall` e
[`agrometeorologiapy`](https://github.com/fcoliveira-utfpr/agrometeorologiapy) (Köppen, Thornthwaite e balanço
hídrico).
