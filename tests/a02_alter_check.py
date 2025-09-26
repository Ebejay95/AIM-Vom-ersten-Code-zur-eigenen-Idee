def test_kind_unter_13(helper):
    """Test: Alter 10 → Kind"""
    modul = helper.import_aufgabe('a02_alter_check')
    output, _ = helper.run_with_input(modul, ['10'])
    assert 'kind' in output.lower(), f"Für Alter 10 sollte 'Kind' stehen: '{output.strip()}'"

def test_jugendlicher_13_17(helper):
    """Test: Alter 16 → Jugendlicher"""
    modul = helper.import_aufgabe('a02_alter_check')
    output, _ = helper.run_with_input(modul, ['16'])
    assert 'jugendlich' in output.lower(), f"Für Alter 16 sollte 'Jugendlicher' stehen: '{output.strip()}'"

def test_erwachsen_18_64(helper):
    """Test: Alter 30 → Erwachsen"""
    modul = helper.import_aufgabe('a02_alter_check')
    output, _ = helper.run_with_input(modul, ['30'])
    assert 'erwachsen' in output.lower(), f"Für Alter 30 sollte 'Erwachsen' stehen: '{output.strip()}'"

def test_rente_ab_65(helper):
    """Test: Alter 70 → Rentenalter"""
    modul = helper.import_aufgabe('a02_alter_check')
    output, _ = helper.run_with_input(modul, ['70'])
    assert any(word in output.lower() for word in ['rent', 'senior']), \
        f"Für Alter 70 sollte 'Rentenalter' stehen: '{output.strip()}'"

def test_grenzwerte(helper):
    """Test: Grenzwerte 13, 18, 65"""
    modul = helper.import_aufgabe('a02_alter_check')
    
    # Alter 13 → Jugendlicher
    output13, _ = helper.run_with_input(modul, ['13'])
    assert 'jugendlich' in output13.lower()
    
    # Alter 18 → Erwachsen  
    output18, _ = helper.run_with_input(modul, ['18'])
    assert 'erwachsen' in output18.lower()
    
    # Alter 65 → Rentenalter
    output65, _ = helper.run_with_input(modul, ['65'])
    assert any(word in output65.lower() for word in ['rent', 'senior'])
