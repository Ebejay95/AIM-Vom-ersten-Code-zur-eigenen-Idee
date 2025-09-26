# Annahme: main() liest Startzahl s und druckt s, s-1, ... 0, danach "Start!".

def test_countdown_5(helper):
    modul = helper.import_aufgabe('a08_countdown')
    output, _ = helper.run_with_input(modul, ['5'])
    low = output.lower()
    assert '5' in output and '0' in output
    assert 'start' in low
