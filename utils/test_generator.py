#!/usr/bin/env python3
"""
Test-Generator für neue Aufgaben.
Aufruf: python utils/test_generator.py a06_neue_aufgabe
"""
import sys
import os

def create_test_template(aufgabe_name):
    """Erstellt ein Test-Template für eine neue Aufgabe."""
    
    title = aufgabe_name.replace('_', ' ').title()
    
    template = f'''# Test für {title}

def test_function_exists(helper):
    """Test: Wichtige Funktionen existieren"""
    modul = helper.import_aufgabe('{aufgabe_name}')
    assert hasattr(modul, 'main'), "Funktion main() fehlt!"

def test_main_works(helper):
    """Test: main() läuft ohne Fehler"""
    modul = helper.import_aufgabe('{aufgabe_name}')
    output, _ = helper.capture_output(modul.main)
    assert len(output.strip()) > 0, "main() sollte eine Ausgabe produzieren"

def test_basic_functionality(helper):
    """Test: Grundfunktionalität (anpassen!)"""
    modul = helper.import_aufgabe('{aufgabe_name}')
    
    # Beispiel mit Input:
    # output, _ = helper.run_with_input(modul, ['test_input'])
    # assert 'erwartete_ausgabe' in output.lower()
    
    # Beispiel ohne Input:
    output, _ = helper.capture_output(modul.main)
    assert len(output) > 0, "Aufgabe sollte eine Ausgabe haben"

# TODO: Weitere spezifische Tests hinzufügen
'''
    
    test_file = f'tests/{aufgabe_name}.py'
    os.makedirs('tests', exist_ok=True)
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"✓ Test-Template erstellt: {test_file}")
    print(f"  Bearbeite die Datei und füge spezifische Tests hinzu!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Aufruf: python utils/test_generator.py <aufgabe_name>")
        print("Beispiel: python utils/test_generator.py a06_grade_ungrade")
        sys.exit(1)
    
    aufgabe_name = sys.argv[1]
    create_test_template(aufgabe_name)
