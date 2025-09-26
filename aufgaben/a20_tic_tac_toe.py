#!/usr/bin/env python3
"""
Aufgabe: Tic-Tac-Toe (CLI, ohne X/GUI)

Tests prüfen NUR die Model-API. Diese Datei enthält zusätzlich
eine einfache Terminal-UI in main().
"""
from __future__ import annotations

# ====== MODEL (vom Test geprüft) ============================================
class TicTacToe:
    def __init__(self) -> None:
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self._finished = False

    def reset(self) -> None:
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self._finished = False

    def available_moves(self) -> list[tuple[int, int]]:
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ' ']

    def make_move(self, row: int, col: int) -> bool:
        if self._finished:
            return False
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        if self.board[row][col] != ' ':
            return False
        self.board[row][col] = self.current_player
        if self.winner() or self.is_draw():
            self._finished = True
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def winner(self) -> str | None:
        b = self.board
        lines = (
            # rows
            b[0], b[1], b[2],
            # cols
            [b[0][0], b[1][0], b[2][0]],
            [b[0][1], b[1][1], b[2][1]],
            [b[0][2], b[1][2], b[2][2]],
            # diagonals
            [b[0][0], b[1][1], b[2][2]],
            [b[0][2], b[1][1], b[2][0]],
        )
        for line in lines:
            if line[0] != ' ' and line.count(line[0]) == 3:
                return line[0]
        return None

    def is_draw(self) -> bool:
        return self.winner() is None and all(cell != ' ' for row in self.board for cell in row)

# ====== CLI (rein Terminal) ================================================
def _render_board(b: list[list[str]]) -> str:
    rows = []
    for r in range(3):
        rows.append(f" {b[r][0]} | {b[r][1]} | {b[r][2]} ")
        if r < 2:
            rows.append("---+---+---")
    return "\n".join(rows)

def main() -> None:
    print("Tic-Tac-Toe (CLI)\nZüge als Zahl 1..9 (oben links = 1, unten rechts = 9) oder 'q' zum Beenden.")
    game = TicTacToe()
    pos_to_rc = {
        '1': (0, 0), '2': (0, 1), '3': (0, 2),
        '4': (1, 0), '5': (1, 1), '6': (1, 2),
        '7': (2, 0), '8': (2, 1), '9': (2, 2),
    }
    while True:
        print()
        print(_render_board(game.board))
        if game.winner():
            print(f"\nSieger: {game.winner()}")
            break
        if game.is_draw():
            print("\nUnentschieden.")
            break
        move = input(f"Spieler {game.current_player}, dein Zug (1-9) oder q: ").strip().lower()
        if move in ('q', 'quit', 'exit'):
            print("Abbruch.")
            break
        if move not in pos_to_rc:
            print("Ungültige Eingabe.")
            continue
        r, c = pos_to_rc[move]
        if not game.make_move(r, c):
            print("Ungültiger Zug (Feld belegt oder Spiel bereits zu Ende).")

if __name__ == "__main__":
    main()
