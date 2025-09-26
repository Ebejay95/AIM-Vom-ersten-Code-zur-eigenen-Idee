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


# Installation

## Was wird benötigt?

- **Git** (zum Klonen des Repositories)
- **Make** (zum Ausführen der Makefile-Befehle)
- **Docker CLI** (Container-Runtime)
- **Colima** (Docker-Alternative, empfohlen)

---

## macOS Installation

### Schritt 1: Homebrew installieren

```bash
# Homebrew installieren (falls noch nicht vorhanden)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# PATH aktualisieren (bei Apple Silicon Macs)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

### Schritt 2: Alle Tools installieren

```bash
# Alle benötigten Tools in einem Befehl
brew install git make colima docker

# Oder einzeln:
brew install git          # Version Control
brew install make         # Build Tool  
brew install colima       # Docker Runtime
brew install docker       # Docker CLI
```

### Schritt 3: Colima starten

```bash
# Colima mit optimalen Einstellungen starten
colima start --cpu 2 --memory 4 --disk 20

# Testen ob alles funktioniert
docker --version
docker run hello-world
```

### Alternative: Ohne Homebrew (manuell)

```bash
# Git (meist schon installiert)
xcode-select --install

# Make (meist schon installiert mit Xcode Tools)
# Falls nicht: xcode-select --install

# Docker CLI
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Colima
curl -LO https://github.com/abiosoft/colima/releases/latest/download/colima-Darwin-x86_64
chmod +x colima-Darwin-x86_64
sudo mv colima-Darwin-x86_64 /usr/local/bin/colima
```

---

## Windows Installation

### Option 1: Chocolatey (Empfohlen)

```powershell
# PowerShell als Administrator öffnen

# Chocolatey installieren
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Alle Tools installieren
choco install git make docker-cli

# WSL2 für Colima
wsl --install
# Neustart erforderlich!

# Nach Neustart: Ubuntu in WSL2 installieren
wsl --install -d Ubuntu

# In WSL2 Ubuntu: Colima installieren
wsl
sudo apt update
wget https://github.com/abiosoft/colima/releases/latest/download/colima-Linux-x86_64
sudo install colima-Linux-x86_64 /usr/local/bin/colima
```

### Option 2: Winget (Windows Package Manager)

```powershell
# In PowerShell
winget install Git.Git
winget install GnuWin32.Make
winget install Docker.DockerCLI

# Für Colima: WSL2 Setup wie oben
```

### Option 3: Manuell

```powershell
# Git installieren
# https://git-scm.com/download/win herunterladen und installieren

# Make installieren (mehrere Optionen):
# 1. Git Bash verwenden (kommt mit Git)
# 2. MSYS2 installieren: https://www.msys2.org/
# 3. Oder Chocolatey make: choco install make

# Docker Desktop (Alternative zu Colima)
# https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe

# WSL2 aktivieren
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
# Neustart erforderlich
```

---

## Linux Installation

### Ubuntu/Debian

```bash
# System aktualisieren
sudo apt update && sudo apt upgrade -y

# Alle Tools installieren
sudo apt install -y git make curl wget

# Docker CLI installieren
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Colima installieren
wget https://github.com/abiosoft/colima/releases/latest/download/colima-Linux-x86_64
sudo install colima-Linux-x86_64 /usr/local/bin/colima

# Neu anmelden für Docker-Rechte
newgrp docker

# Colima starten
colima start --cpu 2 --memory 4 --disk 20

# Testen
git --version
make --version
docker --version
colima version
```

### CentOS/RHEL/Fedora

```bash
# System aktualisieren
sudo dnf update -y

# Tools installieren
sudo dnf install -y git make curl wget

# Docker installieren
sudo dnf install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Colima installieren
curl -LO https://github.com/abiosoft/colima/releases/latest/download/colima-Linux-x86_64
sudo install colima-Linux-x86_64 /usr/local/bin/colima

# Colima starten
colima start --cpu 2 --memory 4 --disk 20
```

### Arch Linux

```bash
# System aktualisieren
sudo pacman -Syu

# Tools installieren
sudo pacman -S git make docker curl wget

# Docker konfigurieren
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Colima installieren
# Option 1: AUR
yay -S colima-bin

# Option 2: Manuell
curl -LO https://github.com/abiosoft/colima/releases/latest/download/colima-Linux-x86_64
sudo install colima-Linux-x86_64 /usr/local/bin/colima

# Colima starten
colima start --cpu 2 --memory 4 --disk 20
```

### openSUSE

```bash
# System aktualisieren
sudo zypper update

# Tools installieren
sudo zypper install git make docker curl wget

# Docker konfigurieren
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Colima installieren
curl -LO https://github.com/abiosoft/colima/releases/latest/download/colima-Linux-x86_64
sudo install colima-Linux-x86_64 /usr/local/bin/colima

# Colima starten
colima start --cpu 2 --memory 4 --disk 20
```

---

## Vollständiger Setup-Test

Nach der Installation auf allen Systemen:

```bash
# 1. Alle Tools prüfen
git --version
make --version
docker --version
colima version

# 2. Repository klonen
git clone <your-python-kurs-repo>
cd python-kurs

# 3. Makefile testen
make version
make status

# 4. Setup vervollständigen
make setup-colima  # Falls Colima nicht läuft
make build         # Python Image bauen
make list          # Aufgaben anzeigen
make run name=hello_world  # Erste Aufgabe testen
```

---

## Troubleshooting nach OS

### macOS Probleme

```bash
# Homebrew PATH Problem
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Make nicht gefunden
xcode-select --install

# Docker Permission Denied
colima restart
```

### Windows Probleme

```powershell
# WSL2 nicht installiert
wsl --install
# Neustart erforderlich

# Make nicht gefunden in PowerShell
# Git Bash verwenden oder MSYS2 installieren

# Docker nicht verfügbar
# In WSL2 arbeiten oder Docker Desktop installieren
```

### Linux Probleme

```bash
# Docker Permission Denied
sudo usermod -aG docker $USER
newgrp docker
# Oder komplett neu anmelden

# Make nicht gefunden
sudo apt install build-essential  # Ubuntu/Debian
sudo dnf install make            # CentOS/RHEL
sudo pacman -S base-devel        # Arch

# Colima startet nicht
# Mehr Speicher zuweisen:
colima start --memory 6 --disk 30
```

---

## Systemanforderungen

### Minimum:
- **RAM:** 4GB (2GB für Colima)
- **Speicher:** 10GB frei
- **CPU:** Dual-Core

### Empfohlen:
- **RAM:** 8GB (4GB für Colima)
- **Speicher:** 20GB frei  
- **CPU:** Quad-Core

### Colima Konfiguration anpassen:

```bash
# Mehr Ressourcen
colima stop
colima start --cpu 4 --memory 6 --disk 30

# Permanente Konfiguration
mkdir -p ~/.colima/default
cat > ~/.colima/default/colima.yaml << EOF
cpu: 4
memory: 6
disk: 30
runtime: docker
EOF
```

---

## Ein-Befehl Setup (wo möglich)

### macOS mit Homebrew:
```bash
curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash && \
brew install git make colima docker && \
colima start --cpu 2 --memory 4 --disk 20
```

### Ubuntu/Debian:
```bash
sudo apt update && sudo apt install -y git make curl && \
curl -fsSL https://get.docker.com | sudo sh && \
sudo usermod -aG docker $USER && \
wget -O- https://github.com/abiosoft/colima/releases/latest/download/colima-Linux-x86_64 | sudo tee /usr/local/bin/colima > /dev/null && \
sudo chmod +x /usr/local/bin/colima
# Neuanmeldung erforderlich für Docker-Gruppe
```

# Colima Container und Volumes bereinigen

## Container stoppen und Colima beenden

```bash
# Alle laufenden Container stoppen
docker stop $(docker ps -q)

# Colima stoppen
colima stop
```

## Alle Volumes löschen

```bash
# Alle unbenutzten Volumes entfernen (löscht alle Daten in Volumes)
docker volume prune -f

# Oder alle Volumes entfernen (auch benannte Volumes)
docker volume rm $(docker volume ls -q)
```

## Komplette Bereinigung

```bash
# Alle Container stoppen
docker stop $(docker ps -q)

# Alle Container entfernen
docker rm $(docker ps -aq)

# Alle Images entfernen
docker rmi $(docker images -q)

# Alle Volumes entfernen
docker volume prune -f

# Alle Netzwerke entfernen
docker network prune -f

# Colima stoppen
colima stop

# Optional: Colima VM komplett löschen
colima delete
```

## ⚠️ Warnung

Diese Befehle löschen **dauerhaft** alle Container, Images und Volume-Daten. Stelle sicher, dass du wichtige Daten gesichert hast, bevor du diese Befehle ausführst.

## Einzelne Schritte erklärt

- `docker stop $(docker ps -q)` - Stoppt alle laufenden Container
- `docker rm $(docker ps -aq)` - Entfernt alle Container (gestoppte und laufende)
- `docker rmi $(docker images -q)` - Entfernt alle Docker Images
- `docker volume prune -f` - Entfernt alle unbenutzten Volumes ohne Nachfrage
- `docker network prune -f` - Entfernt alle unbenutzten Netzwerke ohne Nachfrage
- `colima stop` - Stoppt die Colima VM
- `colima delete` - Löscht die Colima VM komplett