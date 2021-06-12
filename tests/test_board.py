import pandas as pd
import pytest
from tabulate import tabulate
from chess_challenge.chess_board import ChessBoard
from chess_challenge.chess_pieces import (ChessPiece, WhiteKing, WhiteQueen, Pawn,
WhiteBishop, WhiteKnight, WhiteRook, WhitePawn, BlackKing, BlackQueen, 
BlackBishop, BlackKnight, BlackRook, BlackPawn, map_text_piece)

def test_board_dim():
    chessboard = ChessBoard()
    rows = len(chessboard.chessboard)
    cols = len(chessboard.chessboard.columns)
    assert(rows,cols) == (8,8)

def test_obstructions():
    chessboard = ChessBoard()
    chessboard.initialise_game()
    
    rook = chessboard.find_piece_onboard(pos=['A',1], colour='W')
    endpos = (3,'A')
    rook_valid, rook_attack = chessboard.is_valid_move(rook,endpos)

    knight = chessboard.find_piece_onboard(pos=(8,'G'), colour='B')
    endpos = ('H',6)
    knight_valid, knight_attack = chessboard.is_valid_move(knight,endpos)
    assert(rook_valid, rook_attack, knight_valid, knight_attack) == \
        (False, None, True, None)

def test_ruy_lopez_opening():
    chessboard = ChessBoard()
    chessboard.initialise_game()
    turns = ['W','B','W','B','W']
    start_pos = [('E',2), ('E',7),('G',1),('B',8),('F',1)]
    end_pos = [('E',4), ('E',5),('F',3),('C',6),('B',5)]
    
    for start, end, colour in zip(start_pos, end_pos, turns):
        piece = chessboard.find_piece_onboard(start, colour)
        valid_move, attack = chessboard.is_valid_move(piece,end)
        if valid_move is True:
            piece.position = end
            chessboard.chessboard.loc[start[1],start[0]] = None
            chessboard.update_board()

    cols = [chr(i) for i in range(65,73)]
    rows = [i for i in range(8,0,-1)]
    
    board_values = [[None] * len(cols) for i in range(len(rows))]
    syn_chessboard = pd.DataFrame(data=board_values, columns=cols, \
            index=rows)
    black_pawns = [BlackPawn(position=[7,i], unicode=False) \
            for i in syn_chessboard.columns if i!='E']
    black_pawns += [BlackPawn(position=([5,'E']),unicode=False)]
    white_pawns = [WhitePawn(position=[2,i], unicode=False) \
            for i in syn_chessboard.columns if i!='E']
    white_pawns += [WhitePawn(position=([4,'E']),unicode=False)]
    white_queen = WhiteQueen(position=[1,'D'], unicode=False)
    white_king = WhiteKing(position=[1,'E'], unicode=False)
    white_bishops = [WhiteBishop(position=[1,'C'], unicode=False), 
                    WhiteBishop(position=[5,'B'], unicode=False)]
    white_knights = [WhiteKnight(position=[1,'B'], unicode=False),
                    WhiteKnight(position=[3,'F'], unicode=False)]
    white_rooks = [WhiteRook(position=[1,'A'], unicode=False),
                WhiteRook(position=[1,'H'], unicode=False)]
    black_queen = BlackQueen(position=[8,'D'], unicode=False)
    black_king = BlackKing(position=[8,'E'], unicode=False)
    black_bishops = [BlackBishop(position=[8,'C'], unicode=False), 
                    BlackBishop(position=[8,'F'], unicode=False)]
    black_knights = [BlackKnight(position=[6,'C'], unicode=False),
                    BlackKnight(position=[8,'G'], unicode=False)]
    black_rooks = [BlackRook(position=[8,'A'], unicode=False),
                BlackRook(position=[8,'H'], unicode=False)]
    
    army = [white_queen, white_king, \
            white_bishops, white_knights, white_rooks, \
            white_pawns, black_queen, black_king, \
        black_bishops, black_knights, black_rooks, \
        black_pawns]
    
    for setpiece in army:
        if isinstance(setpiece, list):
            for piece in setpiece:
                syn_chessboard.loc[piece.position[0], piece.position[1]] \
                    = piece
        else:
            syn_chessboard.loc[setpiece.position[0], \
                setpiece.position[1]] = setpiece

    printed_syn_chessboard = tabulate(syn_chessboard, headers= cols, 
        showindex='always', tablefmt="fancy_grid", colalign=("center",))
    printed_chessboard = tabulate(chessboard.chessboard, headers= cols, 
        showindex='always', tablefmt="fancy_grid", colalign=("center",))

    assert(printed_syn_chessboard == printed_chessboard)
