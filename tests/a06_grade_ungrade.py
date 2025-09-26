# Annahme: main() liest eine ganze Zahl und gibt "gerade" oder "ungerade" aus.

def test_even(helper):
    modul = helper.import_aufgabe('a06_grade_ungrade')
    output, _ = helper.run_with_input(modul, ['4'])
    assert 'gerade' in output.lower()

def test_odd(helper):
    modul = helper.import_aufgabe('a06_grade_ungrade')
    output, _ = helper.run_with_input(modul, ['7'])
    assert 'ungerade' in output.lower()
