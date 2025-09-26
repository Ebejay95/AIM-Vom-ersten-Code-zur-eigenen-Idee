# Annahme: main() nutzt random.randint(1,100). Wir patchen es auf 42.
# 7 Versuche max. Ausgabe enthält Hinweise "zu hoch/zu niedrig/richtig".

import builtins
import types

def test_guess_sequence(monkeypatch, helper):
    modul = helper.import_aufgabe('a16_zahlenraten_erweitert')

    # Patch random.randint to fixed 42
    import random
    monkeypatch.setattr(random, 'randint', lambda a,b: 42)

    # Versuche: 50 (zu hoch), 25 (zu niedrig), 42 (richtig)
    output, _ = helper.run_with_input(modul, ['50','25','42','n'])
    low = output.lower()
    assert 'hoch' in low
    assert 'niedrig' in low
    assert 'richtig' in low
    # Versuche zählen erwähnt
    assert any(k in low for k in ['versuch', 'versuche'])
