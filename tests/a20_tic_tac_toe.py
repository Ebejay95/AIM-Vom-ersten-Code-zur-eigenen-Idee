def test_model_exists(helper):
    modul = helper.import_aufgabe('a20_tic_tac_toe')
    assert hasattr(modul, 'TicTacToe')

def test_initial_state(helper):
    modul = helper.import_aufgabe('a20_tic_tac_toe')
    g = modul.TicTacToe()
    assert g.current_player == 'X'
    assert len(g.available_moves()) == 9
    assert g.winner() is None and not g.is_draw()

def test_make_move_and_toggle(helper):
    modul = helper.import_aufgabe('a20_tic_tac_toe')
    g = modul.TicTacToe()
    assert g.make_move(0, 0) is True
    assert g.board[0][0] == 'X'
    assert g.current_player == 'O'
    assert g.make_move(0, 0) is False  # belegt
    assert g.make_move(1, 1) is True
    assert g.board[1][1] == 'O'

def test_winner_rows_cols_diags(helper):
    modul = helper.import_aufgabe('a20_tic_tac_toe')
    # Reihe
    g = modul.TicTacToe()
    g.board = [['X','X','X'], [' ','O',' '], [' ',' ','O']]
    assert g.winner() == 'X'
    # Spalte
    g = modul.TicTacToe()
    g.board = [['O','X',' '], ['O','X',' '], ['O',' ','X']]
    assert g.winner() == 'O'
    # Diagonale
    g = modul.TicTacToe()
    g.board = [['X','O','O'], [' ','X',' '], ['O',' ','X']]
    assert g.winner() == 'X'

def test_draw(helper):
    modul = helper.import_aufgabe('a20_tic_tac_toe')
    g = modul.TicTacToe()
    # Klassisches Remis-Brett
    g.board = [
        ['X','O','X'],
        ['X','O','O'],
        ['O','X','X'],
    ]
    assert g.winner() is None
    assert g.is_draw() is True
