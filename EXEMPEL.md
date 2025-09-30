# Användningsexempel / Usage Examples

## Exempel 1: Snabb start med exempel-data

```bash
# Starta programmet
python3 varmekalla_program.py

# I menyn:
# Välj: 7 (Ladda system från fil)
# Ange: exempel_varmesystem.json
# Välj: 5 (Visa sammanfattning)
```

**Resultat:**
```
============================================================
SAMMANFATTNING AV VÄRMESYSTEM
============================================================

Ritningsskala: 1:100.0 (mm)

Antal värmekällor: 2
  1. Värmepump VP1
     - Flöde: 500.0 m³/h
     - Temperatur: 45.0°C
     - Effekt: 5000.0 W
     - Position: (10.5, 20.3)
  2. Luftvärmepump VP2
     - Flöde: 350.0 m³/h
     - Temperatur: 40.0°C
     - Effekt: 3500.0 W
     - Position: (15.2, 18.7)

Antal radiatorer: 3
  1. Radiator Vardagsrum
     - Effekt: 2000.0 W
     - Tilllopp/Frånlopp: 70.0°C / 50.0°C
  2. Radiator Sovrum
     - Effekt: 1500.0 W
     - Tilllopp/Frånlopp: 70.0°C / 50.0°C
  3. Radiator Kök
     - Effekt: 1000.0 W
     - Tilllopp/Frånlopp: 70.0°C / 50.0°C

Total värmeeffekt från värmekällor: 8500 W
Total radiatoreffekt: 4500 W

Effektbalans: +4000 W
✓ Systemet har tillräcklig värmekapacitet
============================================================
```

## Exempel 2: Skapa nytt system från grunden

```bash
python3 varmekalla_program.py
```

### Steg-för-steg:

**1. Sätt ritningsskala**
```
Välj alternativ: 2
Ange skala: 100
Ange enhet: mm
```

**2. Lägg till första värmekällan**
```
Välj alternativ: 3
Namn på värmekälla: Bergvärme BV1
Luftflöde (m³/h): 800
Lufttemperatur (°C): 55
Effekt (W): 8000
Position X: 15.5
Position Y: 22.0
```

**3. Lägg till radiator**
```
Välj alternativ: 4
Namn på radiator: Radiator Hall
Nominell effekt (W): 1200
Tillloppstemperatur (°C): 70
Frånloppstemperatur (°C): 50
Position X: 8.0
Position Y: 12.5
```

**4. Visa sammanfattning**
```
Välj alternativ: 5
```

**5. Spara systemet**
```
Välj alternativ: 6
Filnamn: mitt_varmesystem.json
```

## Exempel 3: Arbeta med PDF-ritning

### Förberedelse
```bash
# Installera PDF-bibliotek
pip install PyPDF2 pdfplumber
```

### Användning
```bash
python3 varmekalla_program.py
```

```
Välj alternativ: 1
Ange sökväg till PDF-fil: /path/to/ritning.pdf
```

Programmet extraherar automatiskt:
- Ritningsskala (t.ex. "SKALA 1:100")
- Effektvärden (W, kW)
- Flöden (m³/h)
- Temperaturer (°C)

## Exempel 4: Analysera PDF-fil direkt

```bash
# Visa vad en PDF innehåller
python3 pdf_helper.py din_ritning.pdf
```

**Resultat:**
```
============================================================
PDF-INFORMATION: din_ritning.pdf
============================================================

✓ Hittad skala: 1:100

✓ Hittade parametrar:
  - effekt_w: 5000.0
  - flode_m3_h: 500.0
  - temperaturer_c: [45.0, 70.0, 50.0]

✓ Text extraherad (1234 tecken)

Första 500 tecken:
------------------------------------------------------------
BYGGRITNING
Projekt: Exempelhus
SKALA 1:100
...
```

## Exempel 5: Programmatisk användning

```python
#!/usr/bin/env python3
from varmekalla_program import Varmekalla, Radiator, VarmesystemManager

# Skapa manager
manager = VarmesystemManager()

# Sätt skala
manager.satt_ritnings_skala(100.0, "mm")

# Lägg till värmekälla
vk = Varmekalla(
    namn="Värmepump 1",
    flode_m3_h=600.0,
    temperatur_c=50.0,
    effekt_w=6000.0,
    position_x=10.0,
    position_y=20.0
)
manager.lagg_till_varmekalla(vk)

# Lägg till radiator
rad = Radiator(
    namn="Radiator 1",
    effekt_w=2000.0,
    temperatur_till_c=70.0,
    temperatur_fran_c=50.0,
    position_x=5.0,
    position_y=10.0
)
manager.lagg_till_radiator(rad)

# Visa sammanfattning
manager.visa_sammanfattning()

# Spara
manager.spara_till_fil("programmatiskt_system.json")
```

## Exempel 6: Kör automatisk demonstration

```bash
# Demonstrerar all funktionalitet
python3 demo.py
```

Detta skapar automatiskt:
- Ett komplett värmesystem
- 2 värmekällor
- 4 radiatorer
- Sammanfattning med effektbalans
- Sparad konfiguration i `demo_varmesystem.json`

## Exempel 7: Testa att allt fungerar

```bash
# Kör alla enhetstester
python3 test_varmekalla.py
```

**Förväntat resultat:**
```
============================================================
KÖR TESTER FÖR VÄRMEKÄLLEHANTERINGSPROGRAM
============================================================

Test: Värmekälla...
✓ Värmekälla test passed
Test: Radiator...
✓ Radiator test passed
Test: RitningsSkala...
✓ RitningsSkala test passed
Test: VarmesystemManager...
✓ VarmesystemManager test passed
Test: Spara och ladda...
✓ Spara och ladda test passed
Test: Ladda exempel_varmesystem.json...
✓ Exempel-fil test passed
Test: PDF helper funktioner...
✓ PDF helper test passed

============================================================
✓ ALLA TESTER LYCKADES!
============================================================
```

## Exempel 8: Redigera JSON-fil direkt

```bash
# Öppna i textredigerare
nano exempel_varmesystem.json
```

```json
{
  "varmekallor": [
    {
      "namn": "Min Värmepump",
      "flode_m3_h": 700.0,
      "temperatur_c": 48.0,
      "effekt_w": 7000.0,
      "position_x": 12.0,
      "position_y": 25.0
    }
  ],
  "radiatorer": [
    {
      "namn": "Min Radiator",
      "effekt_w": 2500.0,
      "temperatur_till_c": 70.0,
      "temperatur_fran_c": 50.0,
      "position_x": 8.0,
      "position_y": 15.0
    }
  ],
  "ritnings_skala": {
    "skala_ratio": 100.0,
    "enhet": "mm"
  }
}
```

Sedan ladda i programmet:
```bash
python3 varmekalla_program.py
# Välj: 7
# Ange: exempel_varmesystem.json
```

## Tips för effektiv användning

### Snabbtangenter i menyn
- Skriv bara siffran och tryck Enter
- Alla värden kan lämnas tomma för standardvärden (där det anges)

### Arbetsflöde för stora projekt
1. Skapa en mall-fil med standardvärden
2. Kopiera och redigera för varje rum/zon
3. Ladda och visa sammanfattning för att kontrollera balans
4. Justera värmekällor eller radiatorer vid behov

### Organisera filer
```
projekt/
  ├── ritning.pdf
  ├── varmesystem_plan1.json
  ├── varmesystem_plan2.json
  └── varmesystem_total.json
```

### Automatisera med script
Skapa egna bash-script för vanliga uppgifter:

```bash
#!/bin/bash
# kontrollera_alla.sh
for fil in varmesystem_*.json; do
    echo "Kontrollerar $fil..."
    python3 -c "
from varmekalla_program import VarmesystemManager
m = VarmesystemManager()
m.ladda_fran_fil('$fil')
m.visa_sammanfattning()
"
done
```

## Fler resurser

- Se `README.md` för fullständig dokumentation
- Se `SNABBSTART.md` för guide och felsökning
- Kör `python3 varmekalla_program.py --help` (kommande funktion)
