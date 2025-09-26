# Annahme: Menü 1=hinzufügen, 2=anzeigen, 3=abhaken, 4=beenden.
# Wir fügen "Milch" hinzu, zeigen Liste, haken Position 1 ab, zeigen erneut.

def test_flow_add_check(helper):
    modul = helper.import_aufgabe('a11_einkaufsliste')
    inputs = ['1', 'Milch', '2', '3', '1', '2', '4']
    output, _ = helper.run_with_input(modul, inputs)
    low = output.lower()
    assert 'milch' in low
    # Irgendein Indikator für "abgehakt" (x) oder "gekauft"
    assert any(k in low for k in ['[x]', 'gekauft', 'abgehakt'])
