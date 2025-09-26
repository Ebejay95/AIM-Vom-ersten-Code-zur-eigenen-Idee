def test_function_exists(helper):
    """Test: hello_world Funktion existiert"""
    modul = helper.import_aufgabe('a00_hello_world')
    assert hasattr(modul, 'hello_world'), "Funktion hello_world() fehlt!"
    assert callable(modul.hello_world), "hello_world ist nicht aufrufbar!"

def test_main_exists(helper):
    """Test: main Funktion existiert"""
    modul = helper.import_aufgabe('a00_hello_world')
    assert hasattr(modul, 'main'), "Funktion main() fehlt!"

def test_hello_output(helper):
    """Test: Ausgabe enthält Begrüßung"""
    modul = helper.import_aufgabe('a00_hello_world')
    output, _ = helper.capture_output(modul.hello_world)
    
    output_lower = output.lower()
    assert any(word in output_lower for word in ['hello', 'hallo', 'welt', 'world']), \
        f"Ausgabe sollte eine Begrüßung enthalten: '{output.strip()}'"

def test_main_works(helper):
    """Test: main() läuft ohne Fehler"""
    modul = helper.import_aufgabe('a00_hello_world')
    output, _ = helper.capture_output(modul.main)
    assert len(output.strip()) > 0, "main() sollte eine Ausgabe produzieren"
