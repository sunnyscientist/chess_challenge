import pytest
from chess_challenge.chess_board import ChessBoard

def test_board_dim():
    chessboard = ChessBoard()
    rows = len(chessboard.chessboard)
    cols = len(chessboard.chessboard.columns)
    assert(rows,cols) == (8,8)

def test_obstructions():
    chessboard = ChessBoard()
    chessboard.initialise_game()
    player_army = chessboard.get_army_location(colour= 'B')        
    opposition_army = chessboard.get_army_location(colour= 'W')
    rook = chessboard.find_piece_onboard(pos=['A',1], colour='B')
    endpos = (3,'A')
    rook_positions = rook.get_unhindered_positions(endpos)
    print(rook_positions)
    valid_move = None
    attack = None
    if rook_positions is None:
        valid_move=False
    else:
        position_idx = rook_positions.index(endpos)
        #iterate through in order of movement to check if any obstructions
        for i in range(position_idx+1):
            if rook_positions[i] in opposition_army or \
                rook_positions[i] in player_army:
                if i < position_idx:
                    valid_move = False
                    break
                elif i == position_idx and \
                    rook_positions[i] in opposition_army:
                    valid_move = True
                    attack = True
                elif i == position_idx and \
                    rook_positions[i] in player_army:
                    valid_move = False
    if valid_move is None:
        valid_move =True

    assert(valid_move, attack) == (False, None)
