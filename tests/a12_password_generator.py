# Annahme: main() liest Länge (int) und gibt ein Passwort mit A-Z, a-z, 0-9 aus.

import re

def test_len_8_charset(helper):
    modul = helper.import_aufgabe('a12_password_generator')
    output, _ = helper.run_with_input(modul, ['8'])
    # Greife das letzte "Wort" >=8 Zeichen aus der Ausgabe
    match = re.findall(r'[A-Za-z0-9]{8,}', output)
    assert match, f"Kein Passwort in Ausgabe gefunden: {output}"
    pwd = match[-1]
    assert len(pwd) >= 8
    assert re.fullmatch(r'[A-Za-z0-9]+', pwd)
