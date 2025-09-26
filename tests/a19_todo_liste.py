# Annahme: Menü:
# 1=hinzufügen, 2=anzeigen, 3=erledigen (index), 4=löschen (index), 5=speichern, 6=beenden.

def test_add_done_delete(helper):
    modul = helper.import_aufgabe('a19_todo_liste')
    inputs = ['1','Hausaufgaben', '2', '3','1', '2', '4','1', '2', '6']
    output, _ = helper.run_with_input(modul, inputs)
    low = output.lower()
    assert 'hausaufgaben' in low
    assert any(k in low for k in ['[x]', 'erledigt'])
    # Nach Löschen sollte die Aufgabe nicht mehr erscheinen (heuristisch)
    assert low.count('hausaufgaben') <= 1
