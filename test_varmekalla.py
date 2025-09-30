#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script för värmekällehanteringsprogram
"""

import sys
import os

# Importera från huvudprogrammet
from varmekalla_program import (
    Varmekalla, Radiator, RitningsSkala, VarmesystemManager
)


def test_varmekalla():
    """Test för Värmekälla-klass"""
    print("Test: Värmekälla...")
    vk = Varmekalla(
        namn="Test VP1",
        flode_m3_h=500.0,
        temperatur_c=45.0,
        effekt_w=5000.0,
        position_x=10.0,
        position_y=20.0
    )
    assert vk.namn == "Test VP1"
    assert vk.flode_m3_h == 500.0
    assert vk.berakna_varmeeffekt() == 5000.0
    print("✓ Värmekälla test passed")


def test_radiator():
    """Test för Radiator-klass"""
    print("Test: Radiator...")
    rad = Radiator(
        namn="Test Radiator",
        effekt_w=2000.0,
        temperatur_till_c=70.0,
        temperatur_fran_c=50.0,
        position_x=5.0,
        position_y=10.0
    )
    assert rad.namn == "Test Radiator"
    assert rad.effekt_w == 2000.0
    assert rad.berakna_varmeoutput() == 2000.0
    print("✓ Radiator test passed")


def test_ritnings_skala():
    """Test för RitningsSkala-klass"""
    print("Test: RitningsSkala...")
    skala = RitningsSkala(skala_ratio=100.0, enhet="mm")
    assert skala.skala_ratio == 100.0
    assert skala.enhet == "mm"
    # 10mm på ritning = 1000mm i verkligheten (1:100)
    assert skala.konvertera_till_verklig_langd(10.0) == 1000.0
    print("✓ RitningsSkala test passed")


def test_varmesystem_manager():
    """Test för VarmesystemManager"""
    print("Test: VarmesystemManager...")
    manager = VarmesystemManager()
    
    # Lägg till värmekälla
    vk = Varmekalla("VP1", 500.0, 45.0, 5000.0, 10.0, 20.0)
    manager.lagg_till_varmekalla(vk)
    assert len(manager.varmekallor) == 1
    
    # Lägg till radiator
    rad = Radiator("Rad1", 2000.0, 70.0, 50.0, 5.0, 10.0)
    manager.lagg_till_radiator(rad)
    assert len(manager.radiatorer) == 1
    
    # Sätt skala
    manager.satt_ritnings_skala(100.0, "mm")
    assert manager.ritnings_skala is not None
    assert manager.ritnings_skala.skala_ratio == 100.0
    
    # Beräkningar
    assert manager.berakna_total_varmeeffekt() == 5000.0
    assert manager.berakna_total_radiatoreffekt() == 2000.0
    
    print("✓ VarmesystemManager test passed")


def test_spara_och_ladda():
    """Test för spara och ladda funktionalitet"""
    print("Test: Spara och ladda...")
    
    # Skapa system
    manager1 = VarmesystemManager()
    vk = Varmekalla("VP1", 500.0, 45.0, 5000.0, 10.0, 20.0)
    rad = Radiator("Rad1", 2000.0, 70.0, 50.0, 5.0, 10.0)
    manager1.lagg_till_varmekalla(vk)
    manager1.lagg_till_radiator(rad)
    manager1.satt_ritnings_skala(100.0, "mm")
    
    # Spara
    test_fil = "/tmp/test_varmesystem.json"
    manager1.spara_till_fil(test_fil)
    assert os.path.exists(test_fil)
    
    # Ladda
    manager2 = VarmesystemManager()
    success = manager2.ladda_fran_fil(test_fil)
    assert success
    assert len(manager2.varmekallor) == 1
    assert len(manager2.radiatorer) == 1
    assert manager2.varmekallor[0].namn == "VP1"
    assert manager2.radiatorer[0].namn == "Rad1"
    assert manager2.ritnings_skala.skala_ratio == 100.0
    
    # Rensa testfil
    os.remove(test_fil)
    
    print("✓ Spara och ladda test passed")


def test_exempel_fil():
    """Test för att ladda exempel-filen"""
    print("Test: Ladda exempel_varmesystem.json...")
    manager = VarmesystemManager()
    success = manager.ladda_fran_fil("exempel_varmesystem.json")
    assert success
    assert len(manager.varmekallor) > 0
    assert len(manager.radiatorer) > 0
    print("✓ Exempel-fil test passed")


def run_all_tests():
    """Kör alla tester"""
    print("\n" + "="*60)
    print("KÖR TESTER FÖR VÄRMEKÄLLEHANTERINGSPROGRAM")
    print("="*60 + "\n")
    
    try:
        test_varmekalla()
        test_radiator()
        test_ritnings_skala()
        test_varmesystem_manager()
        test_spara_och_ladda()
        test_exempel_fil()
        
        print("\n" + "="*60)
        print("✓ ALLA TESTER LYCKADES!")
        print("="*60 + "\n")
        return True
    except AssertionError as e:
        print(f"\n✗ TEST MISSLYCKADES: {e}")
        return False
    except Exception as e:
        print(f"\n✗ FEL: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
