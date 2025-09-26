#!/usr/bin/env python3
"""
Aufgabe: Mini-Pacman (CLI, kein Canvas, kein curses)
- Reines Terminal-Rendering mit ASCII.
- Steuerung: W A S D + ENTER (oder Pfeile als Worte: up/down/left/right)
- Ziel: Alle Punkte (.) essen. Wände = #, leer = ' '.
- Ein einfacher "Geist" G bewegt sich naiv Richtung Spieler.
- Leben: 3. Bei Kollision verliert man 1 Leben und respawnt am Start.

Hinweis: Keine externen Abhängigkeiten; funktioniert überall, wo input()/print() läuft.
"""
from __future__ import annotations
from dataclasses import dataclass
import random
from typing import List, Tuple

Vec = Tuple[int, int]

LEVEL = [
    "#####################",
    "#....#.......#..... #",
    "# ## # ### # # ###  #",
    "#    #     # #      #",
    "#### ##### ### ######",
    "#         P        G#",
    "#####################",
]

@dataclass
class Game:
    grid: List[List[str]]
    w: int
    h: int
    pacman: Vec
    ghost: Vec
    dots: int
    lives: int = 3
    score: int = 0
    start_pos: Vec = (0, 0)

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h

    def is_wall(self, x: int, y: int) -> bool:
        return self.grid[y][x] == '#'

    def set_cell(self, x: int, y: int, ch: str) -> None:
        self.grid[y][x] = ch

    def cell(self, x: int, y: int) -> str:
        return self.grid[y][x]

def load_level(lines: List[str]) -> Game:
    g = [list(row) for row in lines]
    h = len(g)
    w = len(g[0]) if h else 0
    px = py = gx = gy = -1
    dots = 0
    for y in range(h):
        for x in range(w):
            if g[y][x] == 'P':
                px, py = x, y
                g[y][x] = ' '
            elif g[y][x] == 'G':
                gx, gy = x, y
                g[y][x] = ' '
            elif g[y][x] == '.':
                dots += 1
    if px < 0 or gx < 0:
        raise ValueError("Level benötigt einen 'P' (Start) und einen 'G' (Geist).")
    return Game(g, w, h, (px, py), (gx, gy), dots, lives=3, score=0, start_pos=(px, py))

def render(game: Game) -> str:
    # Overlay Pacman/Ghost auf Grid
    out = []
    for y in range(game.h):
        row = []
        for x in range(game.w):
            ch = game.grid[y][x]
            if (x, y) == game.pacman:
                row.append('@')
            elif (x, y) == game.ghost:
                row.append('G')
            else:
                row.append(ch)
        out.append("".join(row))
    hud = f"Score: {game.score}  Leben: {game.lives}  Rest-Punkte: {game.dots}"
    return "\n".join(out) + "\n" + hud

def try_move(game: Game, pos: Vec, delta: Vec) -> Vec:
    nx, ny = pos[0] + delta[0], pos[1] + delta[1]
    if not game.in_bounds(nx, ny) or game.is_wall(nx, ny):
        return pos
    return (nx, ny)

def step_ghost(game: Game) -> None:
    # Naive Greedy-Suche Richtung Pacman (Manhattan-Nähe), mit Random-Tie-Break
    gx, gy = game.ghost
    px, py = game.pacman
    candidates: list[Vec] = []
    if px < gx: candidates.append((-1, 0))
    if px > gx: candidates.append((1, 0))
    if py < gy: candidates.append((0, -1))
    if py > gy: candidates.append((0, 1))
    if not candidates:
        candidates = [(1,0),(-1,0),(0,1),(0,-1)]
    random.shuffle(candidates)
    for dx, dy in candidates:
        nxt = try_move(game, (gx, gy), (dx, dy))
        if nxt != (gx, gy):
            game.ghost = nxt
            return
    # sonst bleibt er stehen

def pick_delta(inp: str) -> Vec:
    s = inp.strip().lower()
    match s:
        case 'w' | 'up': return (0, -1)
        case 's' | 'down': return (0, 1)
        case 'a' | 'left': return (-1, 0)
        case 'd' | 'right': return (1, 0)
        case _: return (0, 0)

def eat_dot_if_any(game: Game) -> None:
    x, y = game.pacman
    if game.cell(x, y) == '.':
        game.set_cell(x, y, ' ')
        game.dots -= 1
        game.score += 10

def collide(game: Game) -> bool:
    return game.pacman == game.ghost

def respawn(game: Game) -> None:
    game.pacman = game.start_pos
    # Ghost zurück auf zufälligen Randpunkt (freies Feld)
    free_edges = []
    for x in range(game.w):
        for y in [0, game.h - 1]:
            if not game.is_wall(x, y):
                free_edges.append((x, y))
    for y in range(game.h):
        for x in [0, game.w - 1]:
            if not game.is_wall(x, y):
                free_edges.append((x, y))
    if free_edges:
        game.ghost = random.choice(free_edges)

def main() -> None:
    random.seed()
    game = load_level(LEVEL)
    print("Mini-Pacman (CLI) – Steuerung: W/A/S/D + ENTER, 'q' beendet.\n")
    while True:
        print("\x1b[H\x1b[2J", end="")  # Bildschirm leeren
        print(render(game))
        if game.dots == 0:
            print("\nGewonnen! Alle Punkte gegessen. 🎉")
            break
        if game.lives <= 0:
            print("\nGame Over.")
            break
        cmd = input("\nZug (w/a/s/d, q=quit): ").strip().lower()
        if cmd in ('q', 'quit', 'exit'):
            print("Abbruch.")
            break

        delta = pick_delta(cmd)
        game.pacman = try_move(game, game.pacman, delta)
        eat_dot_if_any(game)
        step_ghost(game)

        if collide(game):
            game.lives -= 1
            print("\nAutsch! Kollision mit dem Geist. -1 Leben. ENTER für Respawn …")
            input()
            respawn(game)

if __name__ == "__main__":
    main()
