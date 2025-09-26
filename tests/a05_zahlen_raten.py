# Annahme: Feste Zielzahl = 7. Programm fordert wiederholt Eingaben,
# meldet "richtig" bei 7, sonst "falsch" und zeigt die richtige Zahl (optional).

def test_wrong_then_right(helper):
    modul = helper.import_aufgabe('a05_zahlen_raten')
    output, _ = helper.run_with_input(modul, ['5', '7'])
    low = output.lower()
    assert 'falsch' in low
    assert 'richtig' in low
