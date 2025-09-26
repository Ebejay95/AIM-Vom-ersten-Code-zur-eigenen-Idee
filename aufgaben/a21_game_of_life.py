#!/usr/bin/env python3
"""
Aufgabe: Conway's Game of Life (mit Fenster + Startmustern)

Ziel
----
Implementiere die Kernlogik des zellulären Automaten und zeige ihn in einer
kleinen Tkinter-Oberfläche an. Die Tests prüfen ausschließlich die **Logik**.

Regeln (bounded grid)
---------------------
- Wir verwenden einen **begrenzten** Raster (außen ist "tot").
- Für jede Generation:
  - Eine lebende Zelle mit 2 oder 3 Nachbarn überlebt.
  - Eine tote Zelle mit genau 3 Nachbarn wird geboren.
  - Sonst bleibt/ist sie tot.

Core-API (vom Test verwendet)
-----------------------------
- Klasse `LifeGrid(w, h)`:
  - `width`, `height`
  - `set_alive(x, y)`, `set_dead(x, y)`, `is_alive(x, y) -> bool`
  - `clear()`: alles tot
  - `step()`: eine Generation weiter (in-place Update)
  - `seed_pattern(name: str, at: tuple[int,int]=(0,0))`: platziert ein Startmuster
    (case-insensitive). Verfügbare Namen:
      - "blinker", "toad", "beacon", "glider", "lwss" (lightweight spaceship)
  - `alive_cells() -> set[tuple[int,int]]`: Koordinaten lebender Zellen

UI (nicht testrelevant)
-----------------------
- Tkinter-Fenster mit Canvas; Buttons: Start/Stop, Step, Clear, Random, Muster-Auswahl.
- Zellengröße 12–16px ist okay.
- Simulationstakt ~100ms (after).

Hinweise
--------
- Die Tests prüfen: Blinker-Oszillation, Glider-Drift (nach 4 Schritten um (1,1)).
- Achte auf **bounded** Verhalten (kein Wrap-around).
"""

from __future__ import annotations
import random
from dataclasses import dataclass

# ====== MODEL ===============================================================

@dataclass(frozen=True)
class Size:
    width: int
    height: int

class LifeGrid:
    def __init__(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width/height must be positive")
        self.size = Size(width, height)
        self._grid = [[False for _ in range(width)] for _ in range(height)]

    # --- basic ops ---
    @property
    def width(self) -> int:
        return self.size.width

    @property
    def height(self) -> int:
        return self.size.height

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def set_alive(self, x: int, y: int) -> None:
        if self.in_bounds(x, y):
            self._grid[y][x] = True

    def set_dead(self, x: int, y: int) -> None:
        if self.in_bounds(x, y):
            self._grid[y][x] = False

    def is_alive(self, x: int, y: int) -> bool:
        return self.in_bounds(x, y) and self._grid[y][x]

    def clear(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self._grid[y][x] = False

    def alive_cells(self) -> set[tuple[int, int]]:
        return {(x, y) for y in range(self.height) for x in range(self.width) if self._grid[y][x]}

    # --- evolution ---
    def _neighbor_count(self, x: int, y: int) -> int:
        cnt = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                xx, yy = x + dx, y + dy
                if 0 <= xx < self.width and 0 <= yy < self.height and self._grid[yy][xx]:
                    cnt += 1
        return cnt

    def step(self) -> None:
        nxt = [[False for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                n = self._neighbor_count(x, y)
                if self._grid[y][x]:
                    nxt[y][x] = (n == 2 or n == 3)
                else:
                    nxt[y][x] = (n == 3)
        self._grid = nxt

    # --- patterns ---
    def seed_pattern(self, name: str, at: tuple[int, int] = (0, 0)) -> None:
        """
        Platziert ein vordefiniertes Muster mit linkem oberen Offset `at`.
        Namen (case-insensitive): blinker, toad, beacon, glider, lwss
        """
        name = (name or "").strip().lower()
        patterns: dict[str, list[tuple[int, int]]] = {
            # Period 2
            "blinker": [(1, 0), (1, 1), (1, 2)],
            "toad": [(1,1),(2,1),(3,1),(0,2),(1,2),(2,2)],
            "beacon": [(0,0),(1,0),(0,1),(3,2),(2,3),(3,3)],
            # Glider (drift 1,1 pro 4 steps)
            "glider": [(1,0),(2,1),(0,2),(1,2),(2,2)],
            # Lightweight spaceship (LWSS) – 5x4
            "lwss": [(1,0),(2,0),(3,0),(4,0),(0,1),(4,1),(4,2),(0,3),(3,3)],
        }
        coords = patterns.get(name)
        if not coords:
            raise ValueError(f"Unbekanntes Muster: {name}")
        ox, oy = at
        for dx, dy in coords:
            self.set_alive(ox + dx, oy + dy)


# ====== UI (nicht testrelevant) =============================================

def main() -> None:
    try:
        import tkinter as tk
        from tkinter import ttk
    except Exception:
        print("Tkinter nicht verfügbar – die Logikklasse LifeGrid ist trotzdem nutzbar.")
        return

    CELL = 14
    W, H = 50, 30
    running = {"flag": False}

    grid = LifeGrid(W, H)

    root = tk.Tk()
    root.title("Conway's Game of Life")
    canvas = tk.Canvas(root, width=W*CELL, height=H*CELL, bg="white")
    canvas.pack()

    top = tk.Frame(root)
    top.pack(pady=6)

    pattern_var = tk.StringVar(value="glider")
    ttk.Label(top, text="Pattern:").pack(side=tk.LEFT, padx=4)
    ttk.Combobox(top, textvariable=pattern_var, values=["blinker","toad","beacon","glider","lwss"], width=10).pack(side=tk.LEFT)

    def draw():
        canvas.delete("all")
        for (x, y) in grid.alive_cells():
            x0, y0 = x * CELL, y * CELL
            canvas.create_rectangle(x0, y0, x0+CELL, y0+CELL, outline="", fill="black")

    def step():
        grid.step()
        draw()

    def toggle_run():
        running["flag"] = not running["flag"]
        btn_run.config(text="Stop" if running["flag"] else "Start")
        if running["flag"]:
            loop()

    def loop():
        if not running["flag"]:
            return
        grid.step()
        draw()
        root.after(100, loop)

    def do_clear():
        grid.clear()
        draw()

    def do_random():
        grid.clear()
        for y in range(H):
            for x in range(W):
                if random.random() < 0.15:
                    grid.set_alive(x, y)
        draw()

    def place_pattern():
        # platziere zentriert
        name = pattern_var.get()
        grid.clear()
        ox = max(0, W//2 - 5)
        oy = max(0, H//2 - 3)
        try:
            grid.seed_pattern(name, (ox, oy))
        except ValueError:
            pass
        draw()

    btn_run = ttk.Button(top, text="Start", command=toggle_run)
    btn_run.pack(side=tk.LEFT, padx=4)
    ttk.Button(top, text="Step", command=step).pack(side=tk.LEFT, padx=4)
    ttk.Button(top, text="Clear", command=do_clear).pack(side=tk.LEFT, padx=4)
    ttk.Button(top, text="Random", command=do_random).pack(side=tk.LEFT, padx=4)
    ttk.Button(top, text="Pattern", command=place_pattern).pack(side=tk.LEFT, padx=4)

    # Maus: Zellen setzen/löschen
    def on_click(event):
        x, y = event.x // CELL, event.y // CELL
        if grid.in_bounds(x, y):
            if grid.is_alive(x, y):
                grid.set_dead(x, y)
            else:
                grid.set_alive(x, y)
            draw()

    canvas.bind("<Button-1>", on_click)

    draw()
    root.mainloop()


if __name__ == "__main__":
    main()
