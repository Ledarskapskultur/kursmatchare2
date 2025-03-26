# Kursmatchare: UGL-utbildningar

Denna Streamlit-app låter dig matcha deltagarnas önskemål om ort, pris, vecka och restid mot tillgängliga kurser.

## 📄 Format på Excel-filen (kurser)

Din Excel-fil måste innehålla följande kolumner:

- **Vecka** – t.ex. 12
- **Anläggning** – ort/plats där kursen hålls (t.ex. "Göteborg")
- **Arrangör** – t.ex. "CoreCode"
- **Pris** – i SEK (t.ex. 15800)

## ▶️ Så här kör du appen

1. Installera beroenden:
```
pip install -r requirements.txt
```

2. Kör appen:
```
streamlit run app.py
```

## Funktioner

- Ladda upp Excel-fil
- Fyll i deltagarens ort och restid
- Filtrera kurser på vecka, maxpris och restid
- Ladda ner matchat resultat som CSV

