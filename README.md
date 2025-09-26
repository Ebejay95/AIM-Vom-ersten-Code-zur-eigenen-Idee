Python-Kurs (Klasse 9–10) — Docker-Repo
=======================================

Ziel
----
Einfache, einsteigerfreundliche Python-Übungen (absolute Grundlagen) für Klassen 9–10.
Alle Übungen laufen isoliert in einem Docker-Container (Python 3.12).

Inhalte (Auswahl)
-----------------
- hello_world: Erstes Programm mit Ausgabe
- variablen: Einlesen und Addieren von Zahlen
- bedingungen: Wenn/sonst-Entscheidung
- schleifen: Summe von 1 bis n
- strings: Länge, Großschreibung, erster Buchstabe
- listen: Minimum/Maximum/Mittelwert aus einer Liste von Zahlen

Voraussetzungen
---------------
- Docker installiert
- make installiert (macOS/Linux standard; unter Windows z. B. Git Bash/WSL verwenden)

Schnellstart
------------
1) Image bauen:
   make build

2) Übungen auflisten:
   make list

3) Übung ausführen (Beispiel variablen):
   make run name=variablen

4) Lösung ansehen/ausführen:
   make loesung name=variablen

5) Interaktive Shell im Container öffnen:
   make shell

Makefile-Kommandos
------------------
- make build               # Docker-Image erstellen
- make list                # verfügbare Übungsnamen auflisten
- make run name=<name>     # Übung starten (z. B. name=hello_world)
- make loesung name=<name> # Lösung starten
- make shell               # Bash im Container
- make test                # pytest (optional, wenn Tests ergänzt werden)
- make fmt                 # Code formatieren (ruff)

Ordnerstruktur
--------------
.
├─ Dockerfile
├─ Makefile
├─ requirements.txt
├─ README.md
├─ aufgaben/         # Aufgaben (Schüler:innen bearbeiten diese)
│  ├─ hello_world.py
│  ├─ variablen.py
│  ├─ bedingungen.py
│  ├─ schleifen.py
│  ├─ strings.py
│  └─ listen.py
└─ loesungen/        # Beispiel-Lösungen (für Lehrkräfte oder zur Nachsicht)
   ├─ hello_world.py
   ├─ variablen.py
   ├─ bedingungen.py
   ├─ schleifen.py
   ├─ strings.py
   └─ listen.py

Neue Aufgabe anlegen
--------------------
1) Neue Datei unter aufgaben/<name>.py anlegen.
2) (Optional) Passende Lösung unter loesungen/<name>.py ablegen.
3) Ausführen mit:
   make run name=<name>
   bzw. Lösung:
   make loesung name=<name>

Hinweise
--------
- Die Programme können Eingaben über input() erwarten. Beim Ausführen per 'make run ...'
  ist die Session interaktiv (docker -it), d. h. Eingaben funktionieren normal.
- Die Dateien werden per Volume ins Image gemountet. Änderungen sind sofort wirksam.
