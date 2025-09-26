FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# --- Systempakete (als root) ---
# - python3-tk, tk: Tkinter (GUI)
# - build-essential, patchelf: nützlich für PyInstaller / Builds
# - tini: sauberes Signal-Handling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-tk tk \
        build-essential patchelf \
        tini \
    && rm -rf /var/lib/apt/lists/*

# Normalen User anlegen
RUN groupadd -r pyuser && useradd -r -g pyuser pyuser

# Arbeitsverzeichnis
WORKDIR /app
RUN chown pyuser:pyuser /app

# Python-Requirements (als root installieren ist ok)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -f /tmp/requirements.txt

# Auf Non-Root wechseln
USER pyuser

# Tini als Entrypoint (saubere Prozesse)
ENTRYPOINT ["/usr/bin/tini", "--"]

# Quellcode wird zur Laufzeit gemountet; default in eine Shell
CMD ["bash"]
