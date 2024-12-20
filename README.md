[![codecov](https://codecov.io/gh/tkontt/SmartCite/graph/badge.svg?token=TP8CQ2D2LO)](https://codecov.io/gh/tkontt/SmartCite)
# SmartCite
SmartCite

Definition of Done:  
- Vaatimus on analysoitu, suunniteltu, ohjelmoitu, testattu, testaus automatisoitu, dokumentoitu, integroitu muuhun ohjelmistoon ja viety tuotantoympäristöön.

Backlog: 
https://docs.google.com/spreadsheets/d/1wmKJn92xzplfzJKrfDkUWur9-Hx96e_3TWNF-Ajup8c/edit?usp=sharing

Raportti:
https://docs.google.com/document/d/1VrDSSgh54i9A0PbSWo_RU9nWHGxZ7yCTIuv7qEP4IGQ/edit?tab=t.0

## Käynnistysohjeet

Kloonaa repositorio komennolla:
```
git clone
```


Siirry projektin juurihakemistoon.

Luo .env tiedosto ja luo sen sisällöksi:
```
DATABASE_URL=postgresql://XXXX
SECRET_KEY=XXXXX
```


Asenna projektin riippuvuudet komennolla:
```
poetry install
```


Siirry virtuaaliympäristöön komennolla:
```
poetry shell
```


Alusta projektin tietokanta:
```
python src/db_helper.py
```

Käynnistä ohjelma:
```
python src/index.py
```


