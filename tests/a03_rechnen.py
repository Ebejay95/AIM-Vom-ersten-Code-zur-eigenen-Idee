def test_main_exists(helper):
    modul = helper.import_aufgabe('a03_rechnen')
    assert hasattr(modul, 'main')

def test_operations_integers(helper):
    modul = helper.import_aufgabe('a03_rechnen')
    output, _ = helper.run_with_input(modul, ['10', '3'])
    low = output.lower()
    assert '13' in low  # 10+3
    assert '7' in low   # 10-3
    assert '30' in low  # 10*3
    assert '3.33' in low or '3.3' in low or '3,' in low  # 10/3 ~ 3.33

def test_operations_floats(helper):
    modul = helper.import_aufgabe('a03_rechnen')
    output, _ = helper.run_with_input(modul, ['5.5', '2'])
    assert any(s in output for s in ['7.5', '7,5'])