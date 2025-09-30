# Snabbstartsguide / Quick Start Guide

## Snabbstart på 5 minuter

### 1. Starta programmet
```bash
python3 varmekalla_program.py
```

### 2. Prova exemplet
Kör demonstrationsskriptet för att se hur programmet fungerar:
```bash
python3 demo.py
```

### 3. Ladda exempelfil
1. Starta huvudprogrammet: `python3 varmekalla_program.py`
2. Välj alternativ **7** (Ladda system från fil)
3. Ange filnamn: `exempel_varmesystem.json`
4. Välj alternativ **5** (Visa sammanfattning) för att se resultatet

## Vanliga användningsfall

### Skapa ett nytt system från grunden

1. Starta programmet
2. Välj **2** - Sätt ritningsskala (t.ex. 100 för 1:100)
3. Välj **3** - Lägg till värmekällor (en i taget)
   - Ange namn, flöde, temperatur, effekt, position
4. Välj **4** - Lägg till radiatorer (en i taget)
   - Ange namn, effekt, temperaturer, position
5. Välj **5** - Visa sammanfattning för att kontrollera effektbalans
6. Välj **6** - Spara till fil för framtida användning

### Redigera ett befintligt system

1. Välj **7** - Ladda system från fil
2. Välj **3** eller **4** - Lägg till fler komponenter
3. Välj **5** - Visa sammanfattning
4. Välj **6** - Spara med samma eller nytt filnamn

### Använda PDF-ritningar

När du installerat PDF-biblioteken (se nedan), kan du:
1. Välj **1** - Läs parametrar från PDF-ritning
2. Ange sökväg till din PDF-fil
3. Programmet läser automatiskt:
   - Ritningsskala
   - Positioner
   - Tekniska specifikationer (om de finns som text i PDF:en)

## Installation av PDF-stöd

För att läsa PDF-filer, installera nödvändiga bibliotek:

```bash
pip install PyPDF2 pdfplumber
```

### Exempel på PDF-läsning

Skapa en Python-fil med följande kod för att extrahera data från din PDF:

```python
import pdfplumber

# Öppna PDF
with pdfplumber.open("din_ritning.pdf") as pdf:
    # Första sidan
    page = pdf.pages[0]
    
    # Extrahera text
    text = page.extract_text()
    print(text)
    
    # Extrahera tabeller
    tables = page.extract_tables()
    for table in tables:
        print(table)
```

## Tips och tricks

### Effektbalans
- Positiv balans = Överskott av värmeproduktion ✓
- Negativ balans = Underskott - behöver fler värmekällor ⚠

### Positioner i ritning
- Använd X och Y koordinater från ritningen
- Mät från ett fast referenspunkt (t.ex. nedre vänstra hörnet)
- Med skala 1:100 betyder 10mm på ritningen = 1000mm i verkligheten

### Fil-format
- JSON-filer kan redigeras direkt i textredigerare
- Använd UTF-8 för svenska tecken
- Se `exempel_varmesystem.json` för struktur

### Effektberäkningar

**Värmekälla (luftflöde):**
```
Effekt (W) = Luftflöde (m³/h) × Luftdensitet × Specifik värmekapacitet × ΔT
```

**Radiator:**
```
Effekt (W) = Nominell effekt vid standardtemperaturer
```

## Felsökning

### Problem: "ModuleNotFoundError: No module named 'pdfplumber'"
**Lösning:** Installera PDF-bibliotek: `pip install pdfplumber PyPDF2`

### Problem: "File not found"
**Lösning:** Kontrollera sökvägen till filen, använd absolut sökväg om relativ inte fungerar

### Problem: "Encoding error" 
**Lösning:** Kontrollera att filer sparas med UTF-8 encoding

## Exempel på fullständigt arbetsflöde

```bash
# Steg 1: Kör demo för att förstå programmet
python3 demo.py

# Steg 2: Starta huvudprogrammet
python3 varmekalla_program.py

# Steg 3: I programmet, ladda exemplet
# Välj: 7
# Ange: exempel_varmesystem.json

# Steg 4: Lägg till en ny radiator
# Välj: 4
# Ange dina värden

# Steg 5: Se uppdaterad sammanfattning
# Välj: 5

# Steg 6: Spara det uppdaterade systemet
# Välj: 6
# Ange: mitt_varmesystem.json
```

## Support

Programmet innehåller omfattande felhantering och vägledning. Om du stöter på problem:
1. Kontrollera att alla värden är numeriska där det förväntas
2. Se till att filer finns på angivna sökvägar
3. Kör testskriptet: `python3 test_varmekalla.py`

## Nästa steg

- [ ] Utöka PDF-parsing för specifika ritningsformat
- [ ] Lägg till grafisk visualisering av systemet
- [ ] Implementera mer avancerade värmeberäkningar
- [ ] Exportera till CAD-format
- [ ] Lägg till databas för lagring av flera projekt
