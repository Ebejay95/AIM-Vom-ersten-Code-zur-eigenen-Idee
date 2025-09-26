#!/usr/bin/env python3
"""
Aufgabe: Tic-Tac-Toe (mit Fenster)

Ziel
----
Implementiere die Spiellogik (Model) für Tic-Tac-Toe UND eine kleine Tkinter-UI.
Die Tests prüfen NUR die Logik – dein Fenster dient zur Demo für Menschen.

Forderungen (für Tests / Core-API)
----------------------------------
- Klasse `TicTacToe` mit:
  - `board`: 3x3 Liste von Listen; leere Felder sind ' ' (Space).
  - `current_player`: Start ist 'X'; wechselt nach gültigem Zug.
  - `make_move(row, col) -> bool`: Setzt Zeichen des aktuellen Spielers,
    wenn Feld leer und Koordinaten gültig; wechselt anschließend den Spieler;
    gibt True/False zurück je nach Erfolg.
  - `winner() -> str | None`: Gibt 'X' oder 'O' bei Sieg zurück, sonst None.
  - `is_draw() -> bool`: True, wenn Brett voll und kein Sieger.
  - `available_moves() -> list[tuple[int,int]]`: Liste freier Felder (row, col).
  - `reset()`: Setzt Spiel zurück (leer + current_player='X').

UI (nicht testrelevant)
-----------------------
- Ein simples Tkinter-Fenster mit 3x3 Buttons, Status-Label und Reset-Button.
- Klick auf ein Feld ruft `make_move` auf, aktualisiert Text, zeigt Gewinner/Remis.
- Bei Spielende: weitere Züge blockieren, bis Reset.

Hinweis
-------
Die Tests importieren nur die Klasse und nutzen KEIN Tkinter.
Du darfst die UI gern anpassen/verschönern – wichtig ist, dass die Model-API exakt
wie oben funktioniert.
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


# ====== UI (nicht testrelevant) =============================================

def main() -> None:
    try:
        import tkinter as tk
        from tkinter import messagebox
    except Exception:
        # Falls Tk nicht verfügbar ist, einfach CLI-Fallback anzeigen.
        print("Tkinter nicht verfügbar – die Logikklasse TicTacToe ist trotzdem nutzbar.")
        return

    game = TicTacToe()

    root = tk.Tk()
    root.title("Tic-Tac-Toe")

    status = tk.StringVar(value="Spieler: X")

    def refresh():
        status.set(
            f"Sieger: {game.winner()}" if game.winner()
            else ("Unentschieden" if game.is_draw() else f"Spieler: {game.current_player}")
        )
        for r in range(3):
            for c in range(3):
                buttons[r][c]['text'] = game.board[r][c]

    def on_click(r, c):
        if game.make_move(r, c):
            refresh()
            if game.winner():
                messagebox.showinfo("Ende", f"{game.winner()} hat gewonnen!")
            elif game.is_draw():
                messagebox.showinfo("Ende", "Unentschieden!")
        else:
            # optional: kurzer Hinweis
            pass

    def on_reset():
        game.reset()
        refresh()

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()
    buttons = []
    for r in range(3):
        row_widgets = []
        for c in range(3):
            b = tk.Button(frame, text=' ', width=4, height=2, font=("Arial", 24),
                          command=lambda rr=r, cc=c: on_click(rr, cc))
            b.grid(row=r, column=c, padx=5, pady=5)
            row_widgets.append(b)
        buttons.append(row_widgets)

    tk.Label(root, textvariable=status, font=("Arial", 14)).pack(pady=6)
    tk.Button(root, text="Reset", command=on_reset).pack()

    refresh()
    root.mainloop()


if __name__ == "__main__":
    main()
