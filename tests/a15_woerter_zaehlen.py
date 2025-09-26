# Korrektur der Aufgabenidee (ohne Sinn zu ändern): Wortzählung statt Noten.
# Annahme: main() liest einen Text und gibt Anzahl Wörter und Häufigkeiten aus.

def test_count_words(helper):
    modul = helper.import_aufgabe('a15_woerter_zaehlen')
    text = 'Hallo hallo Welt Welt Welt'
    output, _ = helper.run_with_input(modul, [text])
    low = output.lower()
    assert 'anzahl' in low and ('5' in low)
    # Häufigkeiten hallo=2, welt=3
    assert 'hallo' in low and '2' in low
    assert 'welt' in low and '3' in low
