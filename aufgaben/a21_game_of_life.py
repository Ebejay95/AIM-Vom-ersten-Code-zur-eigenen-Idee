#!/usr/bin/env python3
"""
Aufgabe: Conway's Game of Life (CLI, bounded grid, keine GUI/X)

Die Tests prüfen ausschließlich die Logik-Klasse LifeGrid (inkl. seed_pattern).
Hier zusätzlich eine textbasierte main() zum manuellen Spielen/Simulieren.
"""
from __future__ import annotations
import random
from dataclasses import dataclass
from time import sleep

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
        Namen (case-insensitive): blinker, toad, beacon, glider, lwss
        Koordinaten sind relativ zu 'at' (linke obere Ecke).
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

# ====== CLI (rein Terminal) ================================================
def _render(grid: LifeGrid) -> str:
    # 'O' für lebend, '.' für tot
    rows = []
    alive = grid.alive_cells()
    for y in range(grid.height):
        row = []
        for x in range(grid.width):
            row.append('O' if (x, y) in alive else '.')
        rows.append(''.join(row))
    return "\n".join(rows)

def main() -> None:
    print("Conway's Game of Life (CLI)")
    try:
        w = int(input("Breite [50]: ") or "50")
        h = int(input("Höhe   [30]: ") or "30")
    except Exception:
        w, h = 50, 30
    g = LifeGrid(w, h)

    def helptext():
        print("\nKommandos:")
        print("  r <p>     : pattern setzen (blinker|toad|beacon|glider|lwss) zentriert")
        print("  n         : zufällig füllen (15%)")
        print("  c         : clear")
        print("  s [k]     : k Schritte (default 1)")
        print("  a [ms]    : auto-run (ms Delay, default 100) – ENTER stoppt nächsten Prompt")
        print("  t x y     : toggle Zelle (x,y)")
        print("  q         : quit\n")

    helptext()
    while True:
        print(_render(g))
        cmd = input("\n> ").strip().split()
        if not cmd:
            continue
        op = cmd[0].lower()

        if op == 'q':
            break
        elif op == 'c':
            g.clear()
        elif op == 'n':
            g.clear()
            for y in range(g.height):
                for x in range(g.width):
                    if random.random() < 0.15:
                        g.set_alive(x, y)
        elif op == 'r':
            pat = (cmd[1] if len(cmd) > 1 else "glider").lower()
            g.clear()
            ox = max(0, g.width // 2 - 5)
            oy = max(0, g.height // 2 - 3)
            try:
                g.seed_pattern(pat, (ox, oy))
            except ValueError as e:
                print(e)
        elif op == 's':
            k = int(cmd[1]) if len(cmd) > 1 else 1
            for _ in range(max(1, k)):
                g.step()
        elif op == 'a':
            delay = int(cmd[1]) if len(cmd) > 1 else 100
            try:
                while True:
                    g.step()
                    print("\x1b[H\x1b[J", end="")  # clear screen
                    print(_render(g))
                    sleep(max(0.01, delay/1000))
            except KeyboardInterrupt:
                print("\nStop.")
        elif op == 't' and len(cmd) >= 3:
            try:
                x, y = int(cmd[1]), int(cmd[2])
                if g.is_alive(x, y):
                    g.set_dead(x, y)
                else:
                    g.set_alive(x, y)
            except Exception:
                print("Nutze: t x y")
        else:
            helptext()

if __name__ == "__main__":
    main()
