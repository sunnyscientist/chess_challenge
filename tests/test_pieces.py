import pytest
from chess_challenge.chess_pieces import (King, Queen, Bishop, Knight,
Rook, WhitePawn, BlackPawn)

def test_king_movement():
    king = King(position=[4,'G'])
    legal = king.get_unhindered_positions(endposition=[5,'G'])
    illegal = king.get_unhindered_positions(endposition=[2,'A'])
    assert(legal, illegal) == ([(5,'G')],None)

def test_queen_movement():
    queen = Queen(position=[2,'E'])
    legal1 = queen.get_unhindered_positions(endposition=[2,'A'])
    legal2 = queen.get_unhindered_positions(endposition=[5,'H'])
    illegal1 = queen.get_unhindered_positions(endposition=[4,'D'])
    illegal2 = queen.get_unhindered_positions(endposition=[8,'A'])
    assert(legal1, legal2, illegal1, illegal2) == (
        [(2,'D'), (2,'C'),(2,'B'),(2,'A')],
        [(3,'F'), (4,'G'), (5,'H')],
        None,
        None)

def test_bishop_movement():
    bishop = Bishop(position=[2,'B'])
    legal1 = bishop.get_unhindered_positions(endposition=[3,'A'])
    legal2 = bishop.get_unhindered_positions(endposition=[6,'F'])
    illegal1 = bishop.get_unhindered_positions(endposition=[2,'A'])
    illegal2 = bishop.get_unhindered_positions(endposition=[3,'B'])
    assert(legal1, legal2, illegal1, illegal2) == (
        [(3,'A')],
        [(3,'C'), (4,'D'), (5,'E'), (6,'F'),(7,'G'),(8,'H')],
        None,
        None)

def test_knight_movement():
    knight = Knight(position=[8,'G'])
    legal = knight.get_unhindered_positions(endposition=[6,'F'])
    illegal = knight.get_unhindered_positions(endposition=[2,'A'])
    assert(legal, illegal) == (
        [(6,'H'), (6,'F'), (7,'E')],
        None)

def test_rook_movement():
    rook = Rook(position=[3,'E'])
    legal1 = rook.get_unhindered_positions(endposition=[3,'G'])
    legal2 = rook.get_unhindered_positions(endposition=[6,'E'])
    illegal = rook.get_unhindered_positions(endposition=[2,'A'])
    assert(legal1, legal2, illegal) == (
        [(3,'F'), (3,'G'), (3,'H')],
        [(4,'E'), (5,'E'), (6,'E'), (7,'E'), (8,'E')],
        None)

def test_whitepawn_movement():
    whitepawn = WhitePawn(position=[7,'B'])
    legal1 = whitepawn.get_unhindered_positions(endposition=[5,'B'])
    legal2 = whitepawn.get_unhindered_positions(endposition=[6,'A'])
    illegal1 = whitepawn.get_unhindered_positions(endposition=[7,'C'])
    illegal2 = whitepawn.get_unhindered_positions(endposition=[3,'B'])
    assert(legal1, legal2, illegal1, illegal2) == (
        [(6,'B'), (5,'B')],
        [(6,'A')],
        None,
        None)

def test_blackpawn_movement():
    blackpawn = BlackPawn(position=[2,'H'])
    blackpawn.num_moves = 3
    legal1 = blackpawn.get_unhindered_positions(endposition=[3,'H'])
    legal2 = blackpawn.get_unhindered_positions(endposition=[3,'G'])
    illegal1 = blackpawn.get_unhindered_positions(endposition=[4,'H'])
    illegal2 = blackpawn.get_unhindered_positions(endposition=[1,'H'])
    assert(legal1, legal2, illegal1, illegal2) == (
        [(3,'H')],
        [(3,'G')],
        None,
        None)