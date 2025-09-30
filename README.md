# Värmekällehanteringsprogram / Heat Source Management System

Ett program för att hantera värmekällor (via luft med flöde) och radiatorer med möjlighet att läsa in parametrar från PDF-ritningar.

## Funktioner

- ✓ Lägg till och hantera värmekällor (luft med flöde)
- ✓ Lägg till och hantera radiatorer
- ✓ Hantera ritningsskalor från PDF-filer
- ✓ Positionera komponenter baserat på ritning
- ✓ Beräkna total värmeeffekt och balans
- ✓ Spara och ladda systemkonfigurationer
- ✓ Interaktiv meny för enkel användning

## Installation

1. Se till att du har Python 3.7 eller senare installerat
2. Klona detta repository
3. (Valfritt) Installera PDF-bibliotek om du vill läsa PDF-filer:
   ```bash
   pip install -r requirements.txt
   ```

## Användning

### Starta programmet

```bash
python3 varmekalla_program.py
```

### Interaktiv meny

Programmet erbjuder följande alternativ:

1. **Läs parametrar från PDF-ritning** - Läs in skala och parametrar från PDF (kräver PDF-bibliotek)
2. **Sätt ritningsskala manuellt** - Ange skala som 1:100, 1:50 etc.
3. **Lägg till värmekälla** - Lägg till en värmekälla med flöde och effekt
4. **Lägg till radiator** - Lägg till en radiator med effekt och temperaturer
5. **Visa sammanfattning** - Se översikt av hela systemet och effektbalans
6. **Spara system till fil** - Spara konfiguration som JSON
7. **Ladda system från fil** - Ladda tidigare sparat system
8. **Avsluta** - Stäng programmet

### Exempel: Lägg till värmekälla

```
Namn på värmekälla: Värmepump VP1
Luftflöde (m³/h): 500
Lufttemperatur (°C): 45
Effekt (W): 5000
Position X [0]: 10.5
Position Y [0]: 20.3
```

### Exempel: Lägg till radiator

```
Namn på radiator: Radiator Vardagsrum
Nominell effekt (W): 2000
Tillloppstemperatur (°C): 70
Frånloppstemperatur (°C): 50
Position X [0]: 5.0
Position Y [0]: 10.0
```

## Exempel på konfigurationsfil

Se `exempel_varmesystem.json` för ett komplett exempel på hur ett system kan konfigureras.

För att ladda exemplet:
```bash
python3 varmekalla_program.py
# Välj alternativ 7
# Ange filnamn: exempel_varmesystem.json
# Välj alternativ 5 för att se sammanfattning
```

## Systemkomponenter

### Värmekälla (Varmekalla)
- Namn
- Luftflöde (m³/h)
- Temperatur (°C)
- Effekt (W)
- Position (x, y)

### Radiator
- Namn
- Nominell effekt (W)
- Tillloppstemperatur (°C)
- Frånloppstemperatur (°C)
- Position (x, y)

### Ritningsskala (RitningsSkala)
- Skala ratio (t.ex. 100 för 1:100)
- Enhet (mm, cm, m)

## PDF-funktionalitet

Programmet har stöd för att läsa PDF-ritningar. För full funktionalitet, installera:

```bash
pip install PyPDF2 pdfplumber
```

PDF-läsning extraherar:
- Ritningsskala
- Positioner för komponenter
- Tekniska specifikationer

## Effektberäkningar

Programmet beräknar:
- Total värmeeffekt från värmekällor
- Total radiatoreffekt
- Effektbalans (värmeproduktion - värmebehov)

Systemet varnar om radiatoreffekten överstiger värmeproduktionen.

## Filformat

Systemkonfigurationer sparas som JSON med UTF-8-kodning för korrekt hantering av svenska tecken.

## Utveckling

Programmet är skrivet i Python och använder:
- `dataclasses` för datastrukturer
- `json` för serialisering
- `typing` för typannotationer

## Licens

Open source - använd fritt för dina projekt!
