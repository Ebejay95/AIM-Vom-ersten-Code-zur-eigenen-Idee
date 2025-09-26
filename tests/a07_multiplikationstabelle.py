# Annahme: main() liest Zahl n und druckt n x i = Ergebnis für i=1..10.

def test_table_3(helper):
    modul = helper.import_aufgabe('a07_multiplikationstabelle')
    output, _ = helper.run_with_input(modul, ['3'])
    lines = [l for l in output.splitlines() if '3 x ' in l]
    assert len(lines) >= 10
    assert any('3 x 10 = 30' in l for l in lines)
