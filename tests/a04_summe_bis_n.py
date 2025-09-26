# Annahme: main() liest n (int) und druckt die Summe 1..n.

def test_main_exists(helper):
    modul = helper.import_aufgabe('a04_summe_bis_n')
    assert hasattr(modul, 'main')

def test_sum_5(helper):
    modul = helper.import_aufgabe('a04_summe_bis_n')
    output, _ = helper.run_with_input(modul, ['5'])
    assert '15' in output

def test_sum_1(helper):
    modul = helper.import_aufgabe('a04_summe_bis_n')
    output, _ = helper.run_with_input(modul, ['1'])
    assert '1' in output
