def test_model_exists(helper):
    modul = helper.import_aufgabe('a21_game_of_life')
    assert hasattr(modul, 'LifeGrid')

def test_blinker_oscillation(helper):
    modul = helper.import_aufgabe('a21_game_of_life')
    g = modul.LifeGrid(10, 10)
    g.seed_pattern("blinker", at=(4, 4))  # vertikal bei (5,4..6)
    # Zustand 0
    s0 = g.alive_cells().copy()
    # 1 Schritt -> horizontal
    g.step()
    s1 = g.alive_cells().copy()
    # 2. Schritt -> zurück zu s0
    g.step()
    s2 = g.alive_cells().copy()
    assert s0 == s2 and s0 != s1

def test_glider_drift(helper):
    modul = helper.import_aufgabe('a21_game_of_life')
    g = modul.LifeGrid(20, 20)
    g.seed_pattern("glider", at=(2, 2))
    pos0 = g.alive_cells().copy()
    for _ in range(4):
        g.step()
    pos1 = g.alive_cells().copy()
    # Erwartung: Alle Zellen um (1,1) verschoben (innerhalb bounds)
    shifted = {(x+1, y+1) for (x, y) in pos0 if x+1 < g.width and y+1 < g.height}
    # Wegen Boundaries: wir prüfen, dass die Überschneidung der erwarteten
    # Shift-Positionsmenge mit pos1 signifikant ist (alle ursprünglichen passen im 20x20 Grid).
    assert shifted == pos1

def test_seed_invalid_pattern_raises(helper):
    modul = helper.import_aufgabe('a21_game_of_life')
    g = modul.LifeGrid(10, 10)
    try:
        g.seed_pattern("unknown", (0, 0))
        raised = False
    except ValueError:
        raised = True
    assert raised
