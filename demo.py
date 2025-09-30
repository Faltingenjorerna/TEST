#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstrationsskript för värmekällehanteringsprogram
Visar funktionaliteten utan interaktiv användning
"""

from varmekalla_program import Varmekalla, Radiator, VarmesystemManager


def demo_program():
    """Demonstration av programfunktionalitet"""
    print("""
╔════════════════════════════════════════════════════════════╗
║  VÄRMEKÄLLEHANTERING - DEMONSTRATION                       ║
╚════════════════════════════════════════════════════════════╝
""")
    
    # Skapa manager
    manager = VarmesystemManager()
    
    print("1. SÄTTER RITNINGSSKALA")
    print("-" * 60)
    manager.satt_ritnings_skala(100.0, "mm")
    
    print("\n2. LÄGGER TILL VÄRMEKÄLLOR")
    print("-" * 60)
    
    vk1 = Varmekalla(
        namn="Värmepump Entré",
        flode_m3_h=600.0,
        temperatur_c=50.0,
        effekt_w=6000.0,
        position_x=12.5,
        position_y=8.3
    )
    manager.lagg_till_varmekalla(vk1)
    
    vk2 = Varmekalla(
        namn="Luftvärmepump Vardagsrum",
        flode_m3_h=450.0,
        temperatur_c=45.0,
        effekt_w=4500.0,
        position_x=25.0,
        position_y=15.2
    )
    manager.lagg_till_varmekalla(vk2)
    
    print("\n3. LÄGGER TILL RADIATORER")
    print("-" * 60)
    
    rad1 = Radiator(
        namn="Radiator Vardagsrum",
        effekt_w=2500.0,
        temperatur_till_c=70.0,
        temperatur_fran_c=50.0,
        position_x=20.0,
        position_y=12.0
    )
    manager.lagg_till_radiator(rad1)
    
    rad2 = Radiator(
        namn="Radiator Sovrum 1",
        effekt_w=1800.0,
        temperatur_till_c=70.0,
        temperatur_fran_c=50.0,
        position_x=30.0,
        position_y=20.0
    )
    manager.lagg_till_radiator(rad2)
    
    rad3 = Radiator(
        namn="Radiator Sovrum 2",
        effekt_w=1500.0,
        temperatur_till_c=70.0,
        temperatur_fran_c=50.0,
        position_x=10.0,
        position_y=25.0
    )
    manager.lagg_till_radiator(rad3)
    
    rad4 = Radiator(
        namn="Radiator Kök",
        effekt_w=1200.0,
        temperatur_till_c=70.0,
        temperatur_fran_c=50.0,
        position_x=5.0,
        position_y=10.0
    )
    manager.lagg_till_radiator(rad4)
    
    print("\n4. VISAR SAMMANFATTNING AV SYSTEMET")
    print("-" * 60)
    manager.visa_sammanfattning()
    
    print("\n5. SPARAR SYSTEMET TILL FIL")
    print("-" * 60)
    manager.spara_till_fil("demo_varmesystem.json")
    
    print("\n6. DEMONSTRATION AV PDF-LÄSNING (SIMULERAD)")
    print("-" * 60)
    manager.las_parametrar_fran_pdf("ritning_exempel.pdf")
    
    print("""
╔════════════════════════════════════════════════════════════╗
║  DEMONSTRATION SLUTFÖRD                                    ║
║                                                            ║
║  Filen 'demo_varmesystem.json' har skapats.               ║
║  Du kan ladda denna fil från huvudprogrammet.             ║
╚════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    demo_program()
