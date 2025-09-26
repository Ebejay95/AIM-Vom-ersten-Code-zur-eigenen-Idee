# Offen gelassen: Mindestanforderung - es existiert main() und es kommt irgendeine Ausgabe.

def test_main_exists_and_prints(helper):
    modul = helper.import_aufgabe('a20_eigene_idee')
    assert hasattr(modul, 'main')
    output, _ = helper.capture_output(modul.main)
    assert len(output.strip()) > 0
