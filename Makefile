IMAGE_NAME ?= python-kurs
name ?= hello_world
FILE_DIR ?= aufgaben
SOL_DIR ?= loesungen
FILE ?= $(FILE_DIR)/$(name).py
SOLFILE ?= $(SOL_DIR)/$(name).py
PWD := $(shell pwd)

.PHONY: build shell run binary loesung list test fmt clean help check-function check-class

help:
	@echo "Python Kurs - Befehle:"
	@echo "  build                 - Docker-Image bauen"
	@echo "  list                  - Alle Aufgaben auflisten"
	@echo "  run name=<aufgabe>    - Aufgabe ausführen (ruft main() auf)"
	@echo "  binary name=<aufgabe> - Binary aus Aufgabe erstellen"
	@echo "  loesung name=<aufgabe> - Lösung zeigen"
	@echo "  shell                 - Bash im Container"
	@echo "  test                  - Tests ausführen"
	@echo "  fmt                   - Code formatieren"
	@echo "  check-function name=<aufgabe> - Prüft ob Funktion korrekt implementiert"
	@echo "  check-class name=<aufgabe>    - Prüft ob Klasse korrekt implementiert"
	@echo "  clean                 - Docker aufräumen (Container & Images)"

build:
	@docker build -t $(IMAGE_NAME) .

shell:
	@docker run --rm -it -v $(PWD):/app -w /app $(IMAGE_NAME) bash

run:
	@docker run --rm -it -v $(PWD):/app -w /app $(IMAGE_NAME) python -c "from aufgaben.$(name) import main; main()" 2>/dev/null || \
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE_NAME) python -c "from aufgaben.$(name) import *; main()" 2>/dev/null || \
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE_NAME) python $(FILE)

binary:
	@echo "Erstelle Binary für $(name)..."
	@mkdir -p bin
	@docker run --rm -v $(PWD):/app -w /app $(IMAGE_NAME) pyinstaller \
		--onefile \
		--distpath /app/bin \
		--workpath /tmp/build \
		--specpath /tmp \
		--name $(name) \
		$(FILE) 2>/dev/null || \
	docker run --rm -v $(PWD):/app -w /app $(IMAGE_NAME) python -m PyInstaller \
		--onefile \
		--distpath /app/bin \
		--workpath /tmp/build \
		--specpath /tmp \
		--name $(name) \
		$(FILE)
	@echo "✓ Binary erstellt: bin/$(name)"
	@echo "Ausführen mit: ./bin/$(name)"

loesung:
	@echo "Zeige Lösung für $(name)..."
	@docker run --rm -it -v $(PWD):/app -w /app $(IMAGE_NAME) python -c "from loesungen.$(name) import main; main()" 2>/dev/null || \
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE_NAME) python $(SOLFILE)

check-function:
	@echo "Prüfe Funktion in $(name)..."
	@docker run --rm -v $(PWD):/app -w /app $(IMAGE_NAME) python -c "\
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
	@echo "Prüfe Klasse in $(name)..."
	@docker run --rm -v $(PWD):/app -w /app $(IMAGE_NAME) python -c "\
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

list:
	@echo "Verfügbare Aufgaben:"
	@ls $(FILE_DIR) | grep -E '\.py$$' | sed 's/.py$$//' | nl -w2 -s'. '

test:
	@docker run --rm -it -v $(PWD):/app -w /app $(IMAGE_NAME) pytest -q || true

fmt:
	@docker run --rm -it -v $(PWD):/app -w /app $(IMAGE_NAME) ruff format .

clean:
	@echo "Docker aufräumen..."
	@docker ps -q --filter ancestor=$(IMAGE_NAME) | xargs -r docker stop
	@docker ps -aq --filter ancestor=$(IMAGE_NAME) | xargs -r docker rm
	@docker rmi $(IMAGE_NAME) 2>/dev/null || echo "Image $(IMAGE_NAME) nicht gefunden"
	@docker system prune -f
	@echo "Aufräumen abgeschlossen!"
