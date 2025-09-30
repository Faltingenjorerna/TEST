#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program för hantering av värmekällor (luft med flöde) och radiatorer
Heat source management program with PDF parameter input
"""

import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Varmekalla:
    """Värmekälla via luft med flöde (Heat source via air with flow)"""
    namn: str
    flode_m3_h: float  # Luftflöde i m³/h
    temperatur_c: float  # Lufttemperatur i °C
    effekt_w: float  # Effekt i W
    position_x: float = 0.0  # Position i ritning (x-koordinat)
    position_y: float = 0.0  # Position i ritning (y-koordinat)
    
    def berakna_varmeeffekt(self) -> float:
        """Beräkna värmeeffekt från luftflöde"""
        # Förenklad beräkning: använder angiven effekt
        return self.effekt_w


@dataclass
class Radiator:
    """Radiator för värmedistribution"""
    namn: str
    effekt_w: float  # Nominell effekt i W
    temperatur_till_c: float  # Tillloppstemperatur °C
    temperatur_fran_c: float  # Fånloppstemperatur °C
    position_x: float = 0.0  # Position i ritning (x-koordinat)
    position_y: float = 0.0  # Position i ritning (y-koordinat)
    
    def berakna_varmeoutput(self) -> float:
        """Beräkna värmeoutput"""
        return self.effekt_w


@dataclass
class RitningsSkala:
    """Skala för PDF-ritning"""
    skala_ratio: float  # t.ex. 1:100 = 100.0
    enhet: str = "mm"  # Enhet på ritningen
    
    def konvertera_till_verklig_langd(self, ritnings_langd: float) -> float:
        """Konvertera från ritningslängd till verklig längd"""
        return ritnings_langd * self.skala_ratio


class VarmesystemManager:
    """Manager för hela värmesystemet"""
    
    def __init__(self):
        self.varmekallor: List[Varmekalla] = []
        self.radiatorer: List[Radiator] = []
        self.ritnings_skala: Optional[RitningsSkala] = None
        self.ritnings_parametrar: Dict = {}
    
    def lagg_till_varmekalla(self, varmekalla: Varmekalla):
        """Lägg till en värmekälla"""
        self.varmekallor.append(varmekalla)
        print(f"✓ Värmekälla '{varmekalla.namn}' tillagd")
    
    def lagg_till_radiator(self, radiator: Radiator):
        """Lägg till en radiator"""
        self.radiatorer.append(radiator)
        print(f"✓ Radiator '{radiator.namn}' tillagd")
    
    def satt_ritnings_skala(self, skala_ratio: float, enhet: str = "mm"):
        """Sätt ritningsskala från PDF"""
        self.ritnings_skala = RitningsSkala(skala_ratio, enhet)
        print(f"✓ Ritningsskala satt till 1:{skala_ratio} ({enhet})")
    
    def las_parametrar_fran_pdf(self, pdf_fil: str):
        """
        Läs parametrar från PDF-fil
        OBS: Detta är en förenklad implementation. För verklig PDF-läsning
        skulle man använda PyPDF2, pdfplumber eller liknande bibliotek.
        """
        if not os.path.exists(pdf_fil):
            print(f"⚠ Varning: PDF-fil '{pdf_fil}' hittades inte")
            print("  Använd manuell inmatning istället")
            return False
        
        print(f"✓ PDF-fil '{pdf_fil}' hittad")
        
        # Försök importera och använda pdf_helper
        try:
            from pdf_helper import las_pdf_med_pdfplumber, las_pdf_med_pypdf2
            
            # Prova pdfplumber först, fallback till PyPDF2
            data = las_pdf_med_pdfplumber(pdf_fil)
            if not data:
                data = las_pdf_med_pypdf2(pdf_fil)
            
            if data:
                # Sätt skala om hittad
                if data.get('skala'):
                    self.satt_ritnings_skala(data['skala'])
                
                # Spara övriga parametrar
                if data.get('parametrar'):
                    self.ritnings_parametrar.update(data['parametrar'])
                    print(f"✓ Extraherade parametrar: {list(data['parametrar'].keys())}")
                
                print("✓ PDF-parsing genomförd")
                return True
            else:
                print("⚠ Kunde inte extrahera data från PDF")
                return False
                
        except ImportError:
            print("  (PDF-parsing kräver PyPDF2/pdfplumber)")
            print("  Installera med: pip install PyPDF2 pdfplumber")
            return False
        except Exception as e:
            print(f"⚠ Fel vid PDF-läsning: {e}")
            return False
    
    def berakna_total_varmeeffekt(self) -> float:
        """Beräkna total värmeeffekt från alla värmekällor"""
        total = sum(vk.berakna_varmeeffekt() for vk in self.varmekallor)
        return total
    
    def berakna_total_radiatoreffekt(self) -> float:
        """Beräkna total radiatoreffekt"""
        total = sum(rad.berakna_varmeoutput() for rad in self.radiatorer)
        return total
    
    def visa_sammanfattning(self):
        """Visa sammanfattning av systemet"""
        print("\n" + "="*60)
        print("SAMMANFATTNING AV VÄRMESYSTEM")
        print("="*60)
        
        if self.ritnings_skala:
            print(f"\nRitningsskala: 1:{self.ritnings_skala.skala_ratio} ({self.ritnings_skala.enhet})")
        
        print(f"\nAntal värmekällor: {len(self.varmekallor)}")
        for i, vk in enumerate(self.varmekallor, 1):
            print(f"  {i}. {vk.namn}")
            print(f"     - Flöde: {vk.flode_m3_h} m³/h")
            print(f"     - Temperatur: {vk.temperatur_c}°C")
            print(f"     - Effekt: {vk.effekt_w} W")
            print(f"     - Position: ({vk.position_x}, {vk.position_y})")
        
        print(f"\nAntal radiatorer: {len(self.radiatorer)}")
        for i, rad in enumerate(self.radiatorer, 1):
            print(f"  {i}. {rad.namn}")
            print(f"     - Effekt: {rad.effekt_w} W")
            print(f"     - Tilllopp/Frånlopp: {rad.temperatur_till_c}°C / {rad.temperatur_fran_c}°C")
            print(f"     - Position: ({rad.position_x}, {rad.position_y})")
        
        print(f"\nTotal värmeeffekt från värmekällor: {self.berakna_total_varmeeffekt():.0f} W")
        print(f"Total radiatoreffekt: {self.berakna_total_radiatoreffekt():.0f} W")
        
        balans = self.berakna_total_varmeeffekt() - self.berakna_total_radiatoreffekt()
        print(f"\nEffektbalans: {balans:+.0f} W")
        if balans >= 0:
            print("✓ Systemet har tillräcklig värmekapacitet")
        else:
            print("⚠ Varning: Radiatoreffekten överstiger värmeproduktionen")
        
        print("="*60 + "\n")
    
    def spara_till_fil(self, filnamn: str):
        """Spara systemkonfiguration till JSON-fil"""
        data = {
            'varmekallor': [asdict(vk) for vk in self.varmekallor],
            'radiatorer': [asdict(rad) for rad in self.radiatorer],
            'ritnings_skala': asdict(self.ritnings_skala) if self.ritnings_skala else None,
            'ritnings_parametrar': self.ritnings_parametrar
        }
        
        with open(filnamn, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ System sparat till '{filnamn}'")
    
    def ladda_fran_fil(self, filnamn: str):
        """Ladda systemkonfiguration från JSON-fil"""
        if not os.path.exists(filnamn):
            print(f"⚠ Fil '{filnamn}' hittades inte")
            return False
        
        with open(filnamn, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.varmekallor = [Varmekalla(**vk) for vk in data.get('varmekallor', [])]
        self.radiatorer = [Radiator(**rad) for rad in data.get('radiatorer', [])]
        
        skala_data = data.get('ritnings_skala')
        if skala_data:
            self.ritnings_skala = RitningsSkala(**skala_data)
        
        self.ritnings_parametrar = data.get('ritnings_parametrar', {})
        
        print(f"✓ System laddat från '{filnamn}'")
        return True


def interaktiv_meny():
    """Interaktiv meny för att använda programmet"""
    manager = VarmesystemManager()
    
    while True:
        print("\n" + "="*60)
        print("VÄRMESYSTEM - HUVUDMENY")
        print("="*60)
        print("1. Läs parametrar från PDF-ritning")
        print("2. Sätt ritningsskala manuellt")
        print("3. Lägg till värmekälla")
        print("4. Lägg till radiator")
        print("5. Visa sammanfattning")
        print("6. Spara system till fil")
        print("7. Ladda system från fil")
        print("8. Avsluta")
        print("="*60)
        
        val = input("\nVälj alternativ (1-8): ").strip()
        
        if val == '1':
            pdf_fil = input("Ange sökväg till PDF-fil: ").strip()
            manager.las_parametrar_fran_pdf(pdf_fil)
        
        elif val == '2':
            try:
                skala = float(input("Ange skala (t.ex. 100 för 1:100): "))
                enhet = input("Ange enhet (t.ex. mm, cm, m) [mm]: ").strip() or "mm"
                manager.satt_ritnings_skala(skala, enhet)
            except ValueError:
                print("⚠ Ogiltigt värde")
        
        elif val == '3':
            try:
                namn = input("Namn på värmekälla: ").strip()
                flode = float(input("Luftflöde (m³/h): "))
                temp = float(input("Lufttemperatur (°C): "))
                effekt = float(input("Effekt (W): "))
                pos_x = float(input("Position X [0]: ") or "0")
                pos_y = float(input("Position Y [0]: ") or "0")
                
                vk = Varmekalla(namn, flode, temp, effekt, pos_x, pos_y)
                manager.lagg_till_varmekalla(vk)
            except ValueError:
                print("⚠ Ogiltigt värde")
        
        elif val == '4':
            try:
                namn = input("Namn på radiator: ").strip()
                effekt = float(input("Nominell effekt (W): "))
                temp_till = float(input("Tillloppstemperatur (°C): "))
                temp_fran = float(input("Frånloppstemperatur (°C): "))
                pos_x = float(input("Position X [0]: ") or "0")
                pos_y = float(input("Position Y [0]: ") or "0")
                
                rad = Radiator(namn, effekt, temp_till, temp_fran, pos_x, pos_y)
                manager.lagg_till_radiator(rad)
            except ValueError:
                print("⚠ Ogiltigt värde")
        
        elif val == '5':
            manager.visa_sammanfattning()
        
        elif val == '6':
            filnamn = input("Filnamn att spara till [varmesystem.json]: ").strip()
            filnamn = filnamn or "varmesystem.json"
            manager.spara_till_fil(filnamn)
        
        elif val == '7':
            filnamn = input("Filnamn att ladda från: ").strip()
            manager.ladda_fran_fil(filnamn)
        
        elif val == '8':
            print("\nAvslutar programmet...")
            break
        
        else:
            print("⚠ Ogiltigt val, försök igen")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════╗
║  VÄRMEKÄLLEHANTERING - PROGRAM                             ║
║  Heat Source Management System                             ║
╚════════════════════════════════════════════════════════════╝

Detta program hanterar:
  • Värmekällor (luft med flöde)
  • Radiatorer
  • Parametrar från PDF-ritningar
  • Ritningsskalor och positioner
""")
    
    interaktiv_meny()
