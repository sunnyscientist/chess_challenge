import pandas as pd
import itertools

class ChessPiece():
    """Generic Chess Piece"""

    def __init__(self, position, unicode=False):
        self.__position = position
        self.unicode = unicode
        self.symbols = [0, 1]
        self.num_moves = 0
        self.killed = False
    
    @property
    def position(self):
        return self.__position
    
    def __repr__(self):
        if self.unicode is True:
            return "{}".format(self.symbols[1])
        else:
            return "{}".format(self.symbols[0])
    
    def get_unhindered_positions(self):
        pass

    def is_valid_move(self):
        legal_positions = self.get_unhindered_positions()



    #TODO: implement counter to keep track of how many moves
    #TODO: log historical locations

class WhiteChessPiece(ChessPiece):
    """White Chess Piece"""
    def __init__(self, position, unicode=False):
        super().__init__(position,unicode)
        self.colour = 'WHITE'
    
    def state_army(self, chessboard):
        print(chessboard.applymap(type))


class BlackChessPiece(ChessPiece):
    """Black Chess Piece"""

    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.colour = 'BLACK'

    def state_army(self, chessboard):
        print(chessboard.applymap(type))

class Queen(ChessPiece):

    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
    
    def get_unhindered_positions(self):
        current_position = self.position
        legal_positions = []
        for i in range(1,9):
            if i == current_position[0]:
                continue
            legal_positions.append((i,current_position[1]))
        
        #horizontal moves
        for i in range(65,73):
            if chr(i) == current_position[1]:
                continue
            legal_positions.append((current_position[0],chr(i)))
        
        #vertical moves
        for i in range(1,current_position[0]):
            potential_cols = [ord(current_position[1]) + i,\
            ord(current_position[1]) - i]
            potential_cols = [chr(i) for i in potential_cols if 65<=i<=72]
            potential_rows = [current_position[0] + i,\
            current_position[0] - i]
            potential_rows = [i for i in potential_rows if 1<=i<=8]
            legal_positions += list(itertools.product(potential_rows, \
            potential_cols))
        
        #diagonal moves
        for i in range(8,current_position[0],-1):
            potential_cols = [ord(current_position[1]) + i,\
            ord(current_position[1]) - i]
            potential_cols = [chr(i) for i in potential_cols if 65<=i<=72]
            potential_rows = [current_position[0] + i,\
            current_position[0] - i]
            potential_rows = [i for i in potential_rows if 1<=i<=8]
            legal_positions += list(itertools.product(potential_rows, \
            potential_cols))

        return legal_positions

class King(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
    
    def get_unhindered_positions(self):
        current_position = self.position
        potential_rows = [current_position[0]+1, current_position[0]-1, \
            current_position[0]]
        potential_rows = [i for i in potential_rows if 1<=i<=8]
        potential_cols = [ord(current_position[1]) + 1,\
            ord(current_position[1]) - 1, ord(current_position[1])]
        potential_cols = [chr(i) for i in potential_cols if 65<=i<=72]
        legal_positions = list(itertools.product(potential_rows, \
            potential_cols))
        if (current_position[0], current_position[1]) in legal_positions:
            legal_positions.remove((current_position[0], current_position[1]))
        return (legal_positions)

class Bishop(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
    
    def get_unhindered_positions(self):
        """
        Bishops can move diagonally i.e.
        the same number of squares horizontal and vertical
        """
        current_position = self.position
        legal_positions = []

        for i in range(1,current_position[0]):
            potential_cols = [ord(current_position[1]) + i,\
            ord(current_position[1]) - i]
            potential_cols = [chr(i) for i in potential_cols if 65<=i<=72]
            potential_rows = [current_position[0] + i,\
            current_position[0] - i]
            potential_rows = [i for i in potential_rows if 1<=i<=8]
            legal_positions += list(itertools.product(potential_rows, \
            potential_cols))
        
        for i in range(8,current_position[0],-1):
            potential_cols = [ord(current_position[1]) + i,\
            ord(current_position[1]) - i]
            potential_cols = [chr(i) for i in potential_cols if 65<=i<=72]
            potential_rows = [current_position[0] + i,\
            current_position[0] - i]
            potential_rows = [i for i in potential_rows if 1<=i<=8]
            legal_positions += list(itertools.product(potential_rows, \
            potential_cols))
        return (legal_positions)

class Rook(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)

    def get_unhindered_positions(self):
        """
        Rooks can move either horizontally or vertically i.e.
        row or column must stay the same while the other changes
        """
        current_position = self.position
        legal_positions = []
        for i in range(1,9):
            if i == current_position[0]:
                continue
            legal_positions.append((i,current_position[1]))
        
        for i in range(65,73):
            if chr(i) == current_position[1]:
                continue
            legal_positions.append((current_position[0],chr(i)))
        return legal_positions

class Knight(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
    
    def get_unhindered_positions(self, end_position):
        current_position = self.position
        legal_positions = [
            (current_position[0]+2, chr(ord(current_position[1])+1)),
            (current_position[0]+2, chr(ord(current_position[1])-1)),
            (current_position[0]-2, chr(ord(current_position[1])+1)),
            (current_position[0]-2, chr(ord(current_position[1])+-1)),
            (current_position[0]+1, chr(ord(current_position[1])+2)),
            (current_position[0]-1, chr(ord(current_position[1])+2)),
            (current_position[0]-1, chr(ord(current_position[1])-2)),
            (current_position[0]+1, chr(ord(current_position[1])-2))
            ]
        for row,col in legal_positions:
            if 1 <= row <= 8 and 65 <= ord(col) <= 72:
                continue
            else:
                legal_positions.remove((row,col))
        print (legal_positions)

class Pawn(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode) 

class WhiteQueen(Queen,WhiteChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols = ['WQ', u'\u2655']

class WhiteKing(King, WhiteChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols =  ['WK', u'\u2654']

class WhiteBishop(Bishop, WhiteChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols = ['WB', u'\u2657']

class WhiteRook(Rook, WhiteChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols = ['WR', u'\u2656']

class WhiteKnight(Knight, WhiteChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols = ['WKn', u'\u2658']

class WhitePawn(Pawn, WhiteChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols = ['WP', u'\u2659']
    
    def get_unhindered_positions(self):
        current_position = self.position
        legal_positions = [(current_position[0]-1, current_position[1])]
        if self.num_moves == 0:
            legal_positions += [(current_position[0]-2, current_position[1])]
        return legal_positions

class BlackQueen(Queen, BlackChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols = ['BQ', u'\u265B']

class BlackKing(King, BlackChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols = ['BK', u'\u265A']

class BlackBishop(Bishop, BlackChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols = ['BB', u'\u265D']

class BlackRook(Rook, BlackChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols = ['BR', u'\u265C']

class BlackKnight(Knight, BlackChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols = ['BKn', u'\u265E']

class BlackPawn(Pawn,BlackChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.symbols =  ['BP', u'\u265F']
    
    def get_unhindered_positions(self):
        current_position = self.position
        legal_positions = [(current_position[0]+1, current_position[1])]
        if self.num_moves == 0:
            legal_positions += [(current_position[0]+2, current_position[1])]
        return legal_positions

map_text_piece = {'WQ' : WhiteQueen,
                'WK' : WhiteKing,
                'WB' : WhiteBishop,
                'WKn' : WhiteKnight,
                'WR' : WhiteRook,
                'WP' : WhitePawn,
                'BQ' : BlackQueen,
                'BK' : BlackKing,
                'BB' : BlackBishop,
                'BKn' : BlackKnight,
                'BR' : BlackRook,
                'BP' : BlackPawn}

chess_piece_acronyms = {'WQ' : 'White Queen',
                'WK' : 'White King',
                'WB' : 'White Bishop',
                'WKn' : 'White Knight',
                'WR' : 'White Rook',
                'WP' : 'White Pawn',
                'BQ' : 'Black Queen',
                'BK' : 'Black King',
                'BB' : 'Black Bishop',
                'BKn' : 'Black Knight',
                'BR' : 'Black Rook',
                'BP' : 'Black Pawn'}

if __name__ == '__main__':
    bishop = Bishop(position=[4,'C'])
    bishop.get_unhindered_positions([6,'K'])

    king = WhiteKing(position=[1,'E'])
    king.get_unhindered_positions()
    king.get_unhindered_positions()

    rook = BlackRook(position=[3,'C'])
    rook.get_unhindered_positions()
    rook.get_unhindered_positions()
    rook.get_unhindered_positions()

    queen = Queen(position=[4,'D'])
    queen.get_unhindered_positions()

    knight = BlackKnight(position=[4,'E'])
    knight.get_unhindered_positions()