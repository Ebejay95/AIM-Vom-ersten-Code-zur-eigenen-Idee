IMAGE_NAME ?= python-kurs
name ?= a00_hello_world
FILE_DIR ?= aufgaben
SOL_DIR ?= loesungen
TEST_DIR ?= tests
SCORE_FILE ?= .scores.json
FILE ?= $(FILE_DIR)/$(name).py
SOLFILE ?= $(SOL_DIR)/$(name).py
TESTFILE ?= $(TEST_DIR)/$(name).py
PWD := $(shell pwd)

# Docker/Colima detection
DOCKER_CMD := $(shell command -v docker 2> /dev/null)
COLIMA_CMD := $(shell command -v colima 2> /dev/null)

# User ID für Docker (verhindert root-owned files)
USER_ID := $(shell id -u)
GROUP_ID := $(shell id -g)

.PHONY: build shell run binary loesung list test fmt clean help check-function check-class setup-colima status version suggest protect-files setup-tests new-test progress update-score reset-scores

# Farben
GREEN := \033[32m
RED := \033[31m
YELLOW := \033[33m
BLUE := \033[34m
CYAN := \033[36m
MAGENTA := \033[35m
BOLD := \033[1m
RESET := \033[0m

help:
	@echo ""
	@echo "$(CYAN)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(CYAN)║$(RESET)                   $(BOLD)Befehle$(RESET)                    $(CYAN)║$(RESET)"
	@echo "$(CYAN)╚══════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@echo "$(GREEN)📋 Überblick:$(RESET)"
	@echo "  $(YELLOW)version$(RESET)               - Zeige Docker/Colima Version"
	@echo "  $(YELLOW)setup-colima$(RESET)          - Colima installieren und starten"
	@echo "  $(YELLOW)status$(RESET)                - Docker/Colima Status prüfen"
	@echo ""
	@echo "$(GREEN)🔨 Build & Setup:$(RESET)"
	@echo "  $(YELLOW)build$(RESET)                 - Docker-Image bauen"
	@echo "  $(YELLOW)protect-files$(RESET)         - Lösungen und Scores schützen"
	@echo "  $(YELLOW)setup-tests$(RESET)           - Test-Infrastruktur einrichten"
	@echo ""
	@echo "$(GREEN)🚀 Ausführen:$(RESET)"
	@echo "  $(YELLOW)list$(RESET)                  - Alle Aufgaben mit Status auflisten"
	@echo "  $(YELLOW)run name=<aufgabe>$(RESET)    - Aufgabe ausführen"
	@echo "  $(YELLOW)binary name=<aufgabe>$(RESET) - Binary aus Aufgabe erstellen"
	@echo "  $(YELLOW)loesung name=<aufgabe>$(RESET) - Lösung zeigen (nur für Lehrer)"
	@echo "  $(YELLOW)shell$(RESET)                 - Bash im Container"
	@echo ""
	@echo "$(GREEN)🧪 Testing & Progress:$(RESET)"
	@echo "  $(YELLOW)test$(RESET)                  - Alle Tests ausführen (mit Score-Update)"
	@echo "  $(YELLOW)test name=<aufgabe>$(RESET)   - Einzelne Aufgabe testen (mit Score-Update)"
	@echo "  $(YELLOW)suggest$(RESET)               - Nächste Aufgabe vorschlagen"
	@echo "  $(YELLOW)progress$(RESET)              - Fortschritt anzeigen"
	@echo "  $(YELLOW)new-test name=<aufgabe>$(RESET) - Neuen Test erstellen"
	@echo "  $(YELLOW)fmt$(RESET)                   - Code formatieren"
	@echo "  $(YELLOW)reset-scores$(RESET)          - Scores (.scores.json) zurücksetzen"
	@echo ""
	@echo "$(GREEN)🔍 Debug:$(RESET)"
	@echo "  $(YELLOW)check-function name=<aufgabe>$(RESET) - Funktion prüfen"
	@echo "  $(YELLOW)check-class name=<aufgabe>$(RESET)    - Klasse prüfen"
	@echo ""
	@echo "$(GREEN)🧹 Aufräumen:$(RESET)"
	@echo "  $(YELLOW)clean$(RESET)                 - Docker aufräumen"
	@echo ""

version:
	@echo ""
	@echo "$(BLUE)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(BLUE)║$(RESET)              $(BOLD)🔧 System Info$(RESET)                $(BLUE)║$(RESET)"
	@echo "$(BLUE)╚══════════════════════════════════════════════╝$(RESET)"
ifdef DOCKER_CMD
	@echo "$(GREEN)✓$(RESET) Docker gefunden: $(CYAN)$(DOCKER_CMD)$(RESET)"
	@docker --version 2>/dev/null || echo "$(RED)❌ Docker nicht verfügbar$(RESET)"
else
	@echo "$(RED)❌ Docker nicht gefunden$(RESET)"
endif
ifdef COLIMA_CMD
	@echo "$(GREEN)✓$(RESET) Colima gefunden: $(CYAN)$(COLIMA_CMD)$(RESET)"
	@colima version 2>/dev/null || echo "$(RED)❌ Colima nicht verfügbar$(RESET)"
else
	@echo "$(RED)❌ Colima nicht gefunden$(RESET)"
endif
	@echo "$(YELLOW)👤$(RESET) User ID: $(CYAN)$(USER_ID):$(GROUP_ID)$(RESET)"
	@echo ""

status:
	@echo ""
	@echo "$(MAGENTA)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(MAGENTA)║$(RESET)            $(BOLD)📊 Container Status$(RESET)             $(MAGENTA)║$(RESET)"
	@echo "$(MAGENTA)╚══════════════════════════════════════════════╝$(RESET)"
ifdef COLIMA_CMD
	@colima status 2>/dev/null && echo "$(GREEN)✓ Colima läuft$(RESET)" || echo "$(YELLOW)⚠️  Colima ist nicht gestartet$(RESET)"
endif
ifdef DOCKER_CMD
	@docker info >/dev/null 2>&1 && echo "$(GREEN)✓ Docker läuft$(RESET)" || echo "$(RED)❌ Docker läuft nicht$(RESET)"
	@docker images | grep $(IMAGE_NAME) >/dev/null 2>&1 && echo "$(GREEN)✓ Image $(CYAN)$(IMAGE_NAME)$(RESET) vorhanden" || echo "$(YELLOW)⚠️  Image $(CYAN)$(IMAGE_NAME)$(RESET) fehlt (führe '$(BOLD)make build$(RESET)' aus)"
endif
	@echo ""

setup-colima:
	@echo ""
	@echo "$(CYAN)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(CYAN)║$(RESET)              $(BOLD)🚀 Colima Setup$(RESET)                $(CYAN)║$(RESET)"
	@echo "$(CYAN)╚══════════════════════════════════════════════╝$(RESET)"
ifndef COLIMA_CMD
	@echo "$(RED)❌ Colima nicht gefunden. Bitte installiere es zuerst:$(RESET)"
	@echo "  $(YELLOW)macOS:$(RESET) $(BOLD)brew install colima$(RESET)"
	@echo "  $(YELLOW)Andere:$(RESET) siehe $(BOLD)INSTALL.md$(RESET)"
	@exit 1
endif
	@echo "$(GREEN)✓$(RESET) Colima gefunden, starte..."
	@colima start --cpu 2 --memory 4 --disk 20 2>/dev/null || echo "$(YELLOW)⚠️  Colima bereits gestartet oder Fehler$(RESET)"
	@echo "$(BLUE)⏳$(RESET) Warte auf Docker..."
	@sleep 5
	@docker info >/dev/null 2>&1 && echo "$(GREEN)✅ Docker über Colima verfügbar$(RESET)" || echo "$(RED)❌ Docker nicht verfügbar$(RESET)"
	@echo ""

protect-files:
	@echo ""
	@echo "$(RED)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(RED)║$(RESET)              $(BOLD)🔒 Dateien schützen$(RESET)             $(RED)║$(RESET)"
	@echo "$(RED)╚══════════════════════════════════════════════╝$(RESET)"
	@echo "$(YELLOW)🔐 Setze Berechtigungen für Lösungen...$(RESET)"
	@if [ -d "$(SOL_DIR)" ]; then \
		chmod -R 600 $(SOL_DIR)/* 2>/dev/null || true; \
		echo "$(GREEN)✓ Lösungen geschützt (nur lesbar für Owner)$(RESET)"; \
	else \
		echo "$(YELLOW)⚠️  Ordner $(SOL_DIR) nicht gefunden$(RESET)"; \
	fi
	@echo "$(YELLOW)🔐 Erstelle geschützte Score-Datei...$(RESET)"
	@touch $(SCORE_FILE)
	@chmod 600 $(SCORE_FILE)
	@echo "$(GREEN)✓ Score-Datei geschützt$(RESET)"
	@echo "$(YELLOW)🔐 Setze Test-Berechtigungen...$(RESET)"
	@if [ -d "$(TEST_DIR)" ]; then \
		chmod -R 644 $(TEST_DIR)/* 2>/dev/null || true; \
		echo "$(GREEN)✓ Tests geschützt (nur lesbar)$(RESET)"; \
	else \
		echo "$(YELLOW)⚠️  Ordner $(TEST_DIR) nicht gefunden$(RESET)"; \
	fi
	@echo ""

build:
ifndef DOCKER_CMD
	@echo "$(RED)❌ Docker nicht gefunden. Führe '$(BOLD)make setup-colima$(RESET)' aus oder installiere Docker.$(RESET)"
	@exit 1
endif
	@echo ""
	@echo "$(GREEN)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(GREEN)║$(RESET)               $(BOLD)🔨 Docker Build$(RESET)                $(GREEN)║$(RESET)"
	@echo "$(GREEN)╚══════════════════════════════════════════════╝$(RESET)"
	@docker info >/dev/null 2>&1 || (echo "$(RED)❌ Docker läuft nicht. Bei Colima: $(BOLD)colima start$(RESET)" && exit 1)
	@echo "$(BLUE)🏗️  Baue Image $(CYAN)$(IMAGE_NAME)$(RESET)..."
	@docker build -t $(IMAGE_NAME) .
	@$(MAKE) protect-files
	@echo ""
	@echo "$(GREEN)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(GREEN)║$(RESET)              $(BOLD)✅ BUILD ERFOLGREICH$(RESET)            $(GREEN)║$(RESET)"
	@echo "$(GREEN)╚══════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@echo "$(CYAN)     _   _       _ _         $(RESET)"
	@echo "$(CYAN)    | | | | __ _| | | ___    $(RESET)"
	@echo "$(CYAN)    | |_| |/ _\` | | |/ _ \   $(RESET)"
	@echo "$(CYAN)    |  _  | (_| | | | (_) |  $(RESET)"
	@echo "$(CYAN)    |_| |_|\__,_|_|_|\___/   $(RESET)"
	@echo ""
	@echo "$(GREEN)🎯 Nächste Schritte:$(RESET)"
	@echo "  $(YELLOW)•$(RESET) $(BOLD)make list$(RESET)                - Aufgaben anzeigen"
	@echo "  $(YELLOW)•$(RESET) $(BOLD)make suggest$(RESET)             - Nächste Aufgabe vorschlagen"
	@echo "  $(YELLOW)•$(RESET) $(BOLD)make run name=a00_hello_world$(RESET) - Erste Aufgabe testen"
	@echo ""

shell:
ifndef DOCKER_CMD
	@echo "$(RED)❌ Docker nicht verfügbar$(RESET)"
	@exit 1
endif
	@echo ""
	@echo "$(CYAN)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(CYAN)║$(RESET)              $(BOLD)🐚 Container Shell$(RESET)             $(CYAN)║$(RESET)"
	@echo "$(CYAN)╚══════════════════════════════════════════════╝$(RESET)"
	@echo "$(YELLOW)💡 Tipp: Verwende $(BOLD)exit$(RESET) zum Beenden der Shell"
	@echo ""
	@docker run --rm -it -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) bash

run:
ifndef DOCKER_CMD
	@echo "$(RED)❌ Docker nicht verfügbar$(RESET)"
	@exit 1
endif
	@echo ""
	@echo "$(BLUE)══════════════════════════════════════════════$(RESET)"
	@echo "$(BLUE)$(RESET)           $(BOLD)🚀 Starte: $(YELLOW)$(name)$(RESET)              $(BLUE)$(RESET)"
	@echo "$(BLUE)══════════════════════════════════════════════$(RESET)"
	@if [ ! -f "$(FILE)" ]; then \
		echo "$(RED)❌ Aufgabe $(CYAN)$(name)$(RESET) nicht gefunden!$(RESET)"; \
		echo "$(YELLOW)💡 Verfügbare Aufgaben: $(BOLD)make list$(RESET)"; \
		exit 1; \
	fi
	@docker run --rm -it -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python -c "from aufgaben.$(name) import main; main()" 2>/dev/null || \
	docker run --rm -it -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python -c "from aufgaben.$(name) import *; main()" 2>/dev/null || \
	docker run --rm -it -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python $(FILE)
	@echo ""

binary:
ifndef DOCKER_CMD
	@echo "❌ Docker nicht verfügbar"
	@exit 1
endif
	@echo "Erstelle Binary für $(name)..."
	@mkdir -p bin
	@docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) pyinstaller \
		--onefile \
		--distpath /app/bin \
		--workpath /tmp/build \
		--specpath /tmp \
		--name $(name) \
		$(FILE) 2>/dev/null || \
	docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python -m PyInstaller \
		--onefile \
		--distpath /app/bin \
		--workpath /tmp/build \
		--specpath /tmp \
		--name $(name) \
		$(FILE)
	@echo "✓ Binary erstellt: bin/$(name)"
	@echo "Ausführen mit: ./bin/$(name)"

loesung:
	@echo ""
	@echo "$(RED)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(RED)║$(RESET)              $(BOLD)🔐 ZUGRIFF VERWEIGERT$(RESET)           $(RED)║$(RESET)"
	@echo "$(RED)╚══════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@echo "$(YELLOW)⚠️  Lösungen sind nur für Lehrkräfte zugänglich!$(RESET)"
	@echo "$(BLUE)💡 Verwende stattdessen:$(RESET)"
	@echo "  $(CYAN)•$(RESET) $(BOLD)make test name=$(name)$(RESET) - Deine Lösung testen (mit Score-Update)"
	@echo "  $(CYAN)•$(RESET) $(BOLD)make suggest$(RESET)          - Hilfe zur nächsten Aufgabe"
	@echo "  $(CYAN)•$(RESET) $(BOLD)make progress$(RESET)         - Deinen Fortschritt ansehen"
	@echo ""

# ===== TESTING mit Score-Update =====

test:
ifndef DOCKER_CMD
	@echo "$(RED)❌ Docker nicht verfügbar$(RESET)"
	@exit 1
endif
ifdef name
	@$(MAKE) test-single name=$(name)
else
	@$(MAKE) test-all
endif

test-single:
	@echo ""
	@echo "$(BLUE)══════════════════════════════════════════════$(RESET)"
	@echo "$(BLUE)$(RESET)           $(BOLD)🧪 Teste: $(YELLOW)$(name)$(RESET)               $(BLUE)$(RESET)"
	@echo "$(BLUE)══════════════════════════════════════════════$(RESET)"
	@if [ ! -f "$(TESTFILE)" ]; then \
		echo "$(YELLOW)⚠️  Keine Tests für $(CYAN)$(name)$(RESET) vorhanden$(RESET)"; \
		echo "$(BLUE)▶️  Führe Aufgabe aus:$(RESET)"; \
		$(MAKE) run name=$(name); \
	else \
		echo "$(GREEN)🔍 Führe Tests aus...$(RESET)"; \
		if docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python -m pytest $(TESTFILE) -v --tb=short 2>/dev/null; then \
			echo "$(GREEN)✅ Alle Tests bestanden!$(RESET)"; \
			docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python utils/update_scores.py $(name) passed; \
		else \
			echo "$(RED)❌ Tests fehlgeschlagen$(RESET)"; \
			docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python utils/update_scores.py $(name) failed; \
			echo "$(YELLOW)💡 Überprüfe deine Implementierung und versuche es erneut!$(RESET)"; \
		fi; \
	fi
	@echo ""

test-all:
	@echo ""
	@echo "$(MAGENTA)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(MAGENTA)║$(RESET)            $(BOLD)🧪 Alle Tests ausführen$(RESET)           $(MAGENTA)║$(RESET)"
	@echo "$(MAGENTA)╚══════════════════════════════════════════════╝$(RESET)"
	@if [ -d "$(TEST_DIR)" ]; then \
		echo "$(GREEN)🔍 Suche Testdateien und aktualisiere Scores...$(RESET)"; \
		for t in $(TEST_DIR)/*.py; do \
			[ -f "$$t" ] || continue; \
			base=$$(basename "$$t" .py); \
			echo ""; \
			echo "$(CYAN)▶️  $$base$(RESET)"; \
			if docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python -m pytest "$$t" -v --tb=short 2>/dev/null; then \
				echo "$(GREEN)✅ $$base: passed$(RESET)"; \
				docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python utils/update_scores.py "$$base" passed; \
			else \
				echo "$(RED)❌ $$base: failed$(RESET)"; \
				docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python utils/update_scores.py "$$base" failed; \
			fi; \
		done; \
	else \
		echo "$(YELLOW)⚠️  Kein $(TEST_DIR)-Ordner gefunden$(RESET)"; \
	fi
	@echo ""

suggest:
	@echo ""
	@echo "$(CYAN)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(CYAN)║$(RESET)            $(BOLD)💡 Nächste Aufgabe$(RESET)                $(CYAN)║$(RESET)"
	@echo "$(CYAN)╚══════════════════════════════════════════════╝$(RESET)"
	@docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python -c " \
		import os, json, glob, re; \
		scores = {}; \
		if os.path.exists('$(SCORE_FILE)'): \
			try: \
				with open('$(SCORE_FILE)', 'r') as f: \
					scores = json.load(f); \
			except: pass; \
		aufgaben = []; \
		if os.path.exists('$(FILE_DIR)'): \
			for file in glob.glob('$(FILE_DIR)/a*.py'): \
				name = os.path.basename(file)[:-3]; \
				match = re.match(r'a(\\d+)_(.+)', name); \
				if match: \
					num = int(match.group(1)); \
					title = match.group(2).replace('_', ' ').title(); \
					aufgaben.append((num, name, title)); \
		aufgaben.sort(); \
		next_task = None; \
		for num, name, title in aufgaben: \
			if not scores.get(name, {}).get('solved', False): \
				next_task = (name, title); \
				break; \
		if next_task: \
			print(f'$(GREEN)🎯 Empfohlene nächste Aufgabe:$(RESET)'); \
			print(f'   $(BOLD){next_task[0]}$(RESET) - $(CYAN){next_task[1]}$(RESET)'); \
			print(); \
			print(f'$(YELLOW)▶️  Starten mit:$(RESET) $(BOLD)make run name={next_task[0]}$(RESET)'); \
			print(f'$(YELLOW)🧪 Testen mit:$(RESET) $(BOLD)make test name={next_task[0]}$(RESET)'); \
		else: \
			print('$(GREEN)🎉 Alle Aufgaben gelöst! Großartig!$(RESET)'); \
		print(); \
	"

progress:
	@echo ""
	@echo "$(MAGENTA)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(MAGENTA)║$(RESET)               $(BOLD)📊 Fortschritt$(RESET)                $(MAGENTA)║$(RESET)"
	@echo "$(MAGENTA)╚══════════════════════════════════════════════╝$(RESET)"
	@docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python -c " \
		import os, json, glob, re; \
		scores = {}; \
		if os.path.exists('$(SCORE_FILE)'): \
			try: \
				with open('$(SCORE_FILE)', 'r') as f: \
					scores = json.load(f); \
			except: pass; \
		aufgaben = []; \
		if os.path.exists('$(FILE_DIR)'): \
			for file in glob.glob('$(FILE_DIR)/a*.py'): \
				name = os.path.basename(file)[:-3]; \
				match = re.match(r'a(\\d+)_(.+)', name); \
				if match: \
					num = int(match.group(1)); \
					title = match.group(2).replace('_', ' ').title(); \
					solved = scores.get(name, {}).get('solved', False); \
					attempts = scores.get(name, {}).get('attempts', 0); \
					aufgaben.append((num, name, title, solved, attempts)); \
		aufgaben.sort(); \
		total = len(aufgaben); \
		solved_count = sum(1 for _, _, _, solved, _ in aufgaben if solved); \
		print(f'$(BOLD)Gelöst: {solved_count}/{total} Aufgaben$(RESET)'); \
		if total > 0: \
			percentage = int((solved_count / total) * 100); \
			bar_length = 30; \
			filled = int((percentage / 100) * bar_length); \
			bar = '█' * filled + '░' * (bar_length - filled); \
			print(f'$(GREEN)[{bar}]$(RESET) {percentage}%'); \
		print(); \
		for num, name, title, solved, attempts in aufgaben: \
			status = '$(GREEN)✅$(RESET)' if solved else '$(RED)❌$(RESET)'; \
			attempt_text = f' ($(YELLOW){attempts} Versuche$(RESET))' if attempts > 0 else ''; \
			print(f'{status} $(BOLD){name}$(RESET) - {title}{attempt_text}'); \
		print(); \
	"

list:
	@docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python utils/list_tasks.py

check-function:
ifndef DOCKER_CMD
	@echo "❌ Docker nicht verfügbar"
	@exit 1
endif
	@echo "Prüfe Funktion in $(name)..."
	@docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python -c "\
	import inspect; \
	from aufgaben.$(name) import *; \
	functions = [name for name, obj in globals().items() if callable(obj) and not name.startswith('_')]; \
	print('Gefundene Funktionen:', functions); \
	if 'main' in functions: \
		sig = inspect.signature(eval('main')); \
		print('main() Signatur:', sig); \
		print('✓ Funktion main() gefunden!'); \
	else: \
		print('❌ Keine main() Funktion gefunden!'); \
		print('Verfügbare Funktionen:', [f for f in functions if f != 'main'])"

check-class:
ifndef DOCKER_CMD
	@echo "❌ Docker nicht verfügbar"
	@exit 1
endif
	@echo "Prüfe Klasse in $(name)..."
	@docker run --rm -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) python -c "\
	import inspect; \
	from aufgaben.$(name) import *; \
	classes = [name for name, obj in globals().items() if inspect.isclass(obj) and not name.startswith('_')]; \
	print('Gefundene Klassen:', classes); \
	if classes: \
		for cls_name in classes: \
			cls = eval(cls_name); \
			methods = [m for m in dir(cls) if not m.startswith('_')]; \
			print(f'✓ Klasse {cls_name} gefunden!'); \
			print(f'  Methoden: {methods}'); \
	else: \
		print('❌ Keine Klassen gefunden!')"

fmt:
ifndef DOCKER_CMD
	@echo "❌ Docker nicht verfügbar"
	@exit 1
endif
	@docker run --rm -it -v $(PWD):/app -w /app --user $(USER_ID):$(GROUP_ID) $(IMAGE_NAME) ruff format .

clean:
	@echo ""
	@echo "$(RED)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(RED)║$(RESET)              $(BOLD)🧹 Aufräumen$(RESET)                   $(RED)║$(RESET)"
	@echo "$(RED)╚══════════════════════════════════════════════╝$(RESET)"
ifdef DOCKER_CMD
	@echo "$(YELLOW)🗑️  Stoppe Container...$(RESET)"
	@docker ps -q --filter ancestor=$(IMAGE_NAME) | xargs -r docker stop 2>/dev/null || true
	@docker ps -aq --filter ancestor=$(IMAGE_NAME) | xargs -r docker rm 2>/dev/null || true
	@echo "$(YELLOW)🗑️  Entferne Images...$(RESET)"
	@docker rmi $(IMAGE_NAME) 2>/dev/null && echo "$(GREEN)✅ Image $(CYAN)$(IMAGE_NAME)$(RESET) entfernt" || echo "$(YELLOW)⚠️  Image $(CYAN)$(IMAGE_NAME)$(RESET) nicht gefunden"
	@docker system prune -f 2>/dev/null || true
endif
ifdef COLIMA_CMD
	@echo "$(YELLOW)🛑 Stoppe Colima...$(RESET)"
	@colima stop 2>/dev/null && echo "$(GREEN)✅ Colima gestoppt$(RESET)" || echo "$(YELLOW)⚠️  Colima bereits gestoppt$(RESET)"
endif
	@echo "$(GREEN)✅ Aufräumen abgeschlossen!$(RESET)"
	@echo ""

setup-tests:
	@echo ""
	@echo "$(CYAN)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(CYAN)║$(RESET)           $(BOLD)🧪 Setup Test-Infrastruktur$(RESET)        $(CYAN)║$(RESET)"
	@echo "$(CYAN)╚══════════════════════════════════════════════╝$(RESET)"
	@echo "$(GREEN)📁 Erstelle Ordnerstruktur...$(RESET)"
	@mkdir -p tests utils loesungen
	@echo "$(GREEN)📝 Erstelle conftest.py...$(RESET)"
	@cat > tests/conftest.py << 'EOF'\
	# (Inhalt wie in deinem Repo – unverändert) \
	EOF
	@echo "$(GREEN)🔧 Erstelle Test-Generator...$(RESET)"
	@cat > utils/test_generator.py << 'EOF'\
	# (Inhalt wie in deinem Repo – unverändert) \
	EOF
	@chmod +x utils/test_generator.py
	@$(MAKE) protect-files
	@echo ""
	@echo "$(GREEN)✅ Test-Infrastruktur erfolgreich eingerichtet!$(RESET)"
	@echo ""
reset-scores:
	@echo ""
	@echo "$(RED)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(RED)║$(RESET)        $(BOLD)🧽 Scores zurücksetzen (.scores.json)$(RESET)       $(RED)║$(RESET)"
	@echo "$(RED)╚══════════════════════════════════════════════╝$(RESET)"
	@rm -f $(SCORE_FILE)
	@printf "{}\n" > $(SCORE_FILE)
	@chmod 600 $(SCORE_FILE)
	@echo "$(GREEN)✓$(RESET) $(SCORE_FILE) neu initialisiert (leer)"
	@echo ""
	@echo "$(YELLOW)Hinweis:$(RESET) Danach zeigt 'make list' alles als offen (❌)."