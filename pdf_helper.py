#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF-läsningsmodul för värmekällehanteringsprogram
Hjälpmodul för att extrahera parametrar från PDF-ritningar

Kräver: pip install PyPDF2 pdfplumber
"""

import re
from typing import Dict, List, Optional, Tuple


def extrahera_skala_fran_text(text: str) -> Optional[float]:
    """
    Extrahera ritningsskala från text
    
    Exempel:
        "SKALA 1:100" -> 100.0
        "Scale: 1:50" -> 50.0
        "1/100" -> 100.0
    """
    # Sök efter mönster som "1:100", "1/100", "SKALA 1:100"
    patterns = [
        r'skala[:\s]+1[:/](\d+)',
        r'scale[:\s]+1[:/](\d+)',
        r'1[:/](\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    
    return None


def extrahera_parametrar_fran_text(text: str) -> Dict[str, any]:
    """
    Extrahera tekniska parametrar från text
    
    Letar efter:
    - Effekt (W, kW)
    - Flöde (m³/h, l/s)
    - Temperaturer (°C)
    """
    parametrar = {}
    
    # Effekt
    effekt_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:kW|W)', text, re.IGNORECASE)
    if effekt_match:
        effekt_str = effekt_match.group(1).replace(',', '.')
        effekt = float(effekt_str)
        if 'kW' in effekt_match.group(0):
            effekt *= 1000  # Konvertera kW till W
        parametrar['effekt_w'] = effekt
    
    # Flöde
    flode_match = re.search(r'(\d+(?:[.,]\d+)?)\s*m[³3]/h', text, re.IGNORECASE)
    if flode_match:
        flode_str = flode_match.group(1).replace(',', '.')
        parametrar['flode_m3_h'] = float(flode_str)
    
    # Temperatur
    temp_matches = re.findall(r'(\d+(?:[.,]\d+)?)\s*°?C', text, re.IGNORECASE)
    if temp_matches:
        temps = [float(t.replace(',', '.')) for t in temp_matches]
        parametrar['temperaturer_c'] = temps
    
    return parametrar


def las_pdf_med_pdfplumber(pdf_fil: str) -> Dict:
    """
    Läs PDF med pdfplumber (mer robust för moderna PDF:er)
    
    Exempel:
        data = las_pdf_med_pdfplumber("ritning.pdf")
        print(data['skala'])
        print(data['text'])
    """
    try:
        import pdfplumber
    except ImportError:
        print("⚠ pdfplumber är inte installerat. Kör: pip install pdfplumber")
        return {}
    
    try:
        resultat = {
            'skala': None,
            'text': '',
            'tabeller': [],
            'parametrar': {}
        }
        
        with pdfplumber.open(pdf_fil) as pdf:
            # Läs första sidan
            if pdf.pages:
                page = pdf.pages[0]
                
                # Extrahera text
                text = page.extract_text()
                resultat['text'] = text
                
                # Sök efter skala
                if text:
                    skala = extrahera_skala_fran_text(text)
                    if skala:
                        resultat['skala'] = skala
                    
                    # Extrahera parametrar
                    resultat['parametrar'] = extrahera_parametrar_fran_text(text)
                
                # Extrahera tabeller
                tabeller = page.extract_tables()
                resultat['tabeller'] = tabeller
        
        return resultat
    
    except Exception as e:
        print(f"⚠ Fel vid läsning av PDF: {e}")
        return {}


def las_pdf_med_pypdf2(pdf_fil: str) -> Dict:
    """
    Läs PDF med PyPDF2 (grundläggande textextraktion)
    
    Exempel:
        data = las_pdf_med_pypdf2("ritning.pdf")
        print(data['text'])
    """
    try:
        import PyPDF2
    except ImportError:
        print("⚠ PyPDF2 är inte installerat. Kör: pip install PyPDF2")
        return {}
    
    try:
        resultat = {
            'skala': None,
            'text': '',
            'parametrar': {}
        }
        
        with open(pdf_fil, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Läs alla sidor
            all_text = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    all_text.append(text)
            
            full_text = '\n'.join(all_text)
            resultat['text'] = full_text
            
            # Sök efter skala
            skala = extrahera_skala_fran_text(full_text)
            if skala:
                resultat['skala'] = skala
            
            # Extrahera parametrar
            resultat['parametrar'] = extrahera_parametrar_fran_text(full_text)
        
        return resultat
    
    except Exception as e:
        print(f"⚠ Fel vid läsning av PDF: {e}")
        return {}


def hitta_koordinater_i_text(text: str, sokord: str) -> Optional[Tuple[float, float]]:
    """
    Försök hitta koordinater nära ett sökord i texten
    
    Exempel:
        "Värmepump VP1 (10.5, 20.3)" -> (10.5, 20.3)
    """
    # Sök efter mönster som "(10.5, 20.3)" eller "X:10.5 Y:20.3"
    pattern = r'[(\s](\d+(?:[.,]\d+)?)[,\s]+(\d+(?:[.,]\d+)?)[)\s]'
    
    # Hitta text runt sökordet
    sokord_index = text.lower().find(sokord.lower())
    if sokord_index == -1:
        return None
    
    # Sök i text runt sökordet (±100 tecken)
    start = max(0, sokord_index - 100)
    end = min(len(text), sokord_index + 100)
    text_section = text[start:end]
    
    match = re.search(pattern, text_section)
    if match:
        x = float(match.group(1).replace(',', '.'))
        y = float(match.group(2).replace(',', '.'))
        return (x, y)
    
    return None


def visa_pdf_info(pdf_fil: str):
    """
    Visa information om en PDF-fil
    Användbart för att förstå strukturen i PDF:en
    """
    print(f"\n{'='*60}")
    print(f"PDF-INFORMATION: {pdf_fil}")
    print(f"{'='*60}\n")
    
    # Prova pdfplumber först
    data = las_pdf_med_pdfplumber(pdf_fil)
    
    if data:
        if data['skala']:
            print(f"✓ Hittad skala: 1:{data['skala']}")
        else:
            print("⚠ Ingen skala hittad")
        
        if data['parametrar']:
            print(f"\n✓ Hittade parametrar:")
            for key, value in data['parametrar'].items():
                print(f"  - {key}: {value}")
        
        if data['tabeller']:
            print(f"\n✓ Hittade {len(data['tabeller'])} tabell(er)")
            for i, table in enumerate(data['tabeller'], 1):
                print(f"\n  Tabell {i}:")
                for row in table[:5]:  # Visa första 5 raderna
                    print(f"    {row}")
        
        if data['text']:
            print(f"\n✓ Text extraherad ({len(data['text'])} tecken)")
            print(f"\nFörsta 500 tecken:")
            print("-" * 60)
            print(data['text'][:500])
    else:
        print("⚠ Kunde inte läsa PDF-filen")
    
    print(f"\n{'='*60}\n")


# Exempel på användning
if __name__ == "__main__":
    import sys
    
    print("""
╔════════════════════════════════════════════════════════════╗
║  PDF-LÄSNINGSMODUL - TEST                                  ║
╚════════════════════════════════════════════════════════════╝

Detta är en hjälpmodul för att läsa PDF-ritningar.
    """)
    
    # Testa text-extraktion
    exempel_text = """
    BYGGRITNING
    Projekt: Exempelhus
    SKALA 1:100
    
    Värmepump VP1
    Effekt: 5.0 kW
    Flöde: 500 m³/h
    Temperatur: 45°C
    Position: (10.5, 20.3)
    
    Radiator R1
    Effekt: 2000 W
    Tilllopp: 70°C
    Frånlopp: 50°C
    """
    
    print("TEST: Extrahera skala från text")
    skala = extrahera_skala_fran_text(exempel_text)
    print(f"  Resultat: 1:{skala}")
    
    print("\nTEST: Extrahera parametrar från text")
    parametrar = extrahera_parametrar_fran_text(exempel_text)
    print(f"  Resultat: {parametrar}")
    
    print("\nTEST: Hitta koordinater")
    coords = hitta_koordinater_i_text(exempel_text, "VP1")
    print(f"  Resultat: {coords}")
    
    # Om en PDF-fil anges som argument, analysera den
    if len(sys.argv) > 1:
        pdf_fil = sys.argv[1]
        print(f"\n\nAnalyserar PDF-fil: {pdf_fil}")
        visa_pdf_info(pdf_fil)
    else:
        print("\n\nFör att analysera en PDF-fil:")
        print(f"  python3 {sys.argv[0]} <sökväg_till_pdf>")
