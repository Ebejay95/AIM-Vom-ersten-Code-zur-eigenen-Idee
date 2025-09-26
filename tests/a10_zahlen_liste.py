# Annahme: main() liest "1,5,3,9,2" Format, gibt Anzahl, Min, Max, Summe, Durchschnitt aus.

def test_basic_list(helper):
    modul = helper.import_aufgabe('a10_zahlen_liste')
    output, _ = helper.run_with_input(modul, ['1,5,3,9,2'])
    low = output.lower()
    for exp in ['anzahl', 'minimum', 'maximum', 'summe', 'durchschnitt']:
        assert exp in low
    assert '5' in output     # Anzahl
    assert '1' in output     # Min
    assert '9' in output     # Max
    assert '20' in output    # Summe
    assert '4' in output     # Mittel (4.0)
