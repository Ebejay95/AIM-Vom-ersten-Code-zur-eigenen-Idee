# Annahme: Menü: 1=hinzufügen (Name,Telefon,Email), 2=alle, 3=suchen (Name),
# 4=löschen (Name), 5=speichern, 6=laden, 7=beenden.
# Wir fügen, suchen, löschen – Datei I/O ist optional, daher hier nicht getestet.

def test_add_search_delete(helper):
    modul = helper.import_aufgabe('a18_kontaktbuch')
    inputs = [
        '1', 'Max Mustermann', '0123', 'max@test.de',
        '2',
        '3', 'Max',
        '4', 'Max Mustermann',
        '2',
        '7'
    ]
    output, _ = helper.run_with_input(modul, inputs)
    low = output.lower()
    assert 'max' in low and '0123' in low
    assert 'gelöscht' in low or 'entfernt' in low
