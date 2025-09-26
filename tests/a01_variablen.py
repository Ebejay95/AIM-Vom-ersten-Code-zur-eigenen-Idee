def test_addiere_zahlen_exists(helper):
    """Test: addiere_zahlen Funktion existiert"""
    modul = helper.import_aufgabe('a01_variablen')
    # Flexibel - kann auch direkt in main() implementiert sein
    assert hasattr(modul, 'main'), "main() Funktion fehlt!"

def test_addition_simple(helper):
    """Test: Einfache Addition 5 + 3 = 8"""
    modul = helper.import_aufgabe('a01_variablen')
    output, _ = helper.run_with_input(modul, ['5', '3'])
    assert '8' in output, f"Summe von 5+3=8 nicht gefunden in: '{output.strip()}'"

def test_addition_zero(helper):
    """Test: Addition mit 0"""
    modul = helper.import_aufgabe('a01_variablen')
    output, _ = helper.run_with_input(modul, ['0', '7'])
    assert '7' in output, f"Summe von 0+7=7 nicht gefunden in: '{output.strip()}'"

def test_addition_large_numbers(helper):
    """Test: Addition größerer Zahlen"""
    modul = helper.import_aufgabe('a01_variablen')
    output, _ = helper.run_with_input(modul, ['100', '200'])
    assert '300' in output, f"Summe von 100+200=300 nicht gefunden in: '{output.strip()}'"
