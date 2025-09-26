# Annahme: Menü 1=Note hinzufügen, 2=anzeigen, 3=Durchschnitt, 4=Beenden.
# Wir fügen 2, 4, 1 hinzu, zeigen, berechnen Durchschnitt.

def test_notes_flow(helper):
    modul = helper.import_aufgabe('a14_notenverwaltung')
    inputs = ['1','2', '1','4', '1','1', '2', '3', '4']
    output, _ = helper.run_with_input(modul, inputs)
    low = output.lower()
    assert '2' in output and '4' in output and '1' in output
    # Durchschnitt (2+4+1)/3 = 2.33...
    assert any(x in low for x in ['2.33', '2,33', '2.3'])
