# Annahme (Präzisierung): main() fragt nacheinander: Zahl1, Operator (+,-,*,/), Zahl2.
# Gibt das Ergebnis aus. Wiederholung ist optional; wir testen einen Durchlauf.

def test_addition(helper):
    modul = helper.import_aufgabe('a13_taschenrechner')
    output, _ = helper.run_with_input(modul, ['10', '+', '5'])
    assert '15' in output

def test_division(helper):
    modul = helper.import_aufgabe('a13_taschenrechner')
    output, _ = helper.run_with_input(modul, ['7', '/', '2'])
    assert any(x in output for x in ['3.5', '3,5'])
