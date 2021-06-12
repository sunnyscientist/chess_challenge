import pytest
from chess_challenge.chess_board import ChessBoard

def test_board_dim():
    chessboard = ChessBoard()
    rows = len(chessboard.chessboard)
    cols = len(chessboard.chessboard.columns)
    assert(rows,cols) == (8,8)
