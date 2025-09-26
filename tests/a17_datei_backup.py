# Annahme: main() fragt nach Dateiname, erstellt eine Kopie mit Zeitstempel
# im Namen, fügt Zeilennummern hinzu und druckt Anzahl Zeilen.

import os
import re

def test_backup_creates_file(tmp_path, monkeypatch, helper):
    src = tmp_path / 'test.txt'
    src.write_text('a\nb\nc\n', encoding='utf-8')
    monkeypatch.chdir(tmp_path)

    modul = helper.import_aufgabe('a17_datei_backup')
    output, _ = helper.run_with_input(modul, [str(src.name)])
    low = output.lower()
    assert 'backup' in low or 'kopie' in low
    assert '3' in output  # 3 Zeilen

    # Prüfe, dass eine neue Datei entstanden ist
    backups = [p for p in tmp_path.iterdir() if p.name != src.name]
    assert backups, "Keine Backup-Datei gefunden"
    content = backups[0].read_text(encoding='utf-8')
    assert content.startswith('1:') and '3:' in content
