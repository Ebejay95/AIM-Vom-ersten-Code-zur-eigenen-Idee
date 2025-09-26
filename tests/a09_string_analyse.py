# Annahme: main() liest einen Text und gibt Länge, Groß/Klein,
# ersten/letzten Buchstaben und Palindrom-Info aus.

def test_hallo(helper):
    modul = helper.import_aufgabe('a09_string_analyse')
    output, _ = helper.run_with_input(modul, ['Hallo'])
    low = output.lower()
    assert '5' in output               # Länge
    assert 'hallo' in low              # klein
    assert 'hallo' != 'Hallo'          # sanity
    assert 'h' in low and 'o' in low   # erster/letzter Buchstabe erwähnt
    assert 'palindrom' in low and ('nein' in low or 'false' in low)

def test_palindrom(helper):
    modul = helper.import_aufgabe('a09_string_analyse')
    output, _ = helper.run_with_input(modul, ['Reliefpfeiler'])
    low = output.lower()
    assert 'palindrom' in low and ('ja' in low or 'true' in low)
