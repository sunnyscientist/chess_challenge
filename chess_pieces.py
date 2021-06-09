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
        self.can_jump = False
    
    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position
    
    def __repr__(self):
        if self.unicode is True:
            return "{}".format(self.symbols[1])
        else:
            return "{}".format(self.symbols[0])
    
    def get_unhindered_positions(self, endposition):
        pass

    def remove_invalid_positions(self, potential_positions):
        pass

    def is_valid_move(self):
        potential_positions = self.get_unhindered_positions()
    
    @staticmethod
    def pos_within_bounds(position):
        if type(position[0]) == int:
            row,col = position
        else:
            col,row = position
        
        if not 1<=row<=8:
            return False
        if not 65<=ord(col)<=72:
            return False
        return True

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
    
    def get_unhindered_positions(self, endposition):
        current_position = self.position
        potential_positions = {
                        'left' : [], 
                        'right' : [], 
                        'up' : [], 
                        'down' : [], 
                        'diag1' : [],
                        'diag2' : []
                        }
        #vertical moves
        for i in range(1,9):
            if i == current_position[0]:
                continue
            if i< current_position[0]:
                potential_positions['down'].append((i,current_position[1]))
            else:
                potential_positions['up'].append((i,current_position[1]))
        
        #horizontal moves
        for i in range(65,73):
            if chr(i) == current_position[1]:
                continue
            if i < ord(current_position[1]):
                potential_positions['left'].append((current_position[0],chr(i)))
            else:
                potential_positions['right'].append((current_position[0],chr(i)))
        
        for i in range(1,current_position[0]+1):
            potential_cols = [ord(current_position[1]) + i,\
            ord(current_position[1]) - i]
            potential_cols = [chr(i) for i in potential_cols if 65<=i<=72]
            potential_rows = [current_position[0] + i,\
            current_position[0] - i]
            potential_rows = [i for i in potential_rows if 1<=i<=8]
            potential_positions['diag1'] += list(itertools.product(potential_rows, \
            potential_cols))
        
        #diagonal moves
        for i in range(8,current_position[0]-1,-1):
            potential_cols = [ord(current_position[1]) + i,\
            ord(current_position[1]) - i]
            potential_cols = [chr(i) for i in potential_cols if 65<=i<=72]
            
            potential_rows = [current_position[0] + i,\
            current_position[0] - i]
            potential_rows = [i for i in potential_rows if 1<=i<=8]
            
            potential_positions['diag2'] += list(itertools.product(potential_rows, \
            potential_cols))
        
        for direction, square in potential_positions.items():
            if tuple(endposition) in square:
                return potential_positions[direction]
        # TODO: sort diaognal values
    
    def find_legal_moves(self, army_map):
        #remove positions which are occupied by same colour
        pass

class King(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
    
    def get_unhindered_positions(self, endposition):
        current_position = self.position
        
        potential_rows = [current_position[0]+1, current_position[0]-1, \
            current_position[0]]
        potential_rows = [i for i in potential_rows if 1<=i<=8]
        potential_cols = [ord(current_position[1]) + 1,\
            ord(current_position[1]) - 1, ord(current_position[1])]
        potential_cols = [chr(i) for i in potential_cols if 65<=i<=72]
        
        potential_positions = list(itertools.product(potential_rows, \
            potential_cols))
        
        if (current_position[0], current_position[1]) in potential_positions:
            potential_positions.remove((current_position[0], current_position[1]))
        
        if tuple(endposition) in potential_positions:
            return potential_positions

class Bishop(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
    
    def get_unhindered_positions(self, endposition):
        """
        Bishops can move diagonally i.e.
        the same number of squares horizontal and vertical
        """
        current_position = self.position
        potential_positions = {'diag1' : [],'diag2' : []}

        for i in range(1,current_position[0]+1):
            potential_cols = [ord(current_position[1]) + i,\
            ord(current_position[1]) - i]
            potential_cols = [chr(i) for i in potential_cols if 65<=i<=72]
            
            potential_rows = [current_position[0] + i,\
            current_position[0] - i]
            potential_rows = [i for i in potential_rows if 1<=i<=8]
            
            potential_positions['diag1'] += sorted(list(itertools.product( \
                potential_rows,potential_cols)), key=lambda x:x[0])
        
        for i in range(8,current_position[0]-1,-1):
            potential_cols = [ord(current_position[1]) + i,\
            ord(current_position[1]) - i]
            potential_cols = [chr(i) for i in potential_cols if 65<=i<=72]
            
            potential_rows = [current_position[0] + i,\
            current_position[0] - i]
            potential_rows = [i for i in potential_rows if 1<=i<=8]
            
            potential_positions['diag2'] += sorted(list(itertools.product( \
                potential_rows,potential_cols)), key=lambda x:x[0])
        
        for direction, square in potential_positions.items():
            print(square)
            if tuple(endposition) in square:
                return potential_positions[direction]
        
        # TODO: sprt diaognal values

class Rook(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)

    def get_unhindered_positions(self, endposition):
        """
        Rooks can move either horizontally or vertically i.e.
        row or column must stay the same while the other changes
        """
        current_position = self.position
        potential_positions = potential_positions = {
                        'left' : [], 
                        'right' : [],
                        'up' : [], 
                        'down' : []
                        }
        for i in range(1,9):
            if i == current_position[0]:
                continue
            if i< current_position[0]:
                potential_positions['down'].append((i,current_position[1]))
            else:
                potential_positions['up'].append((i,current_position[1]))
        
        #horizontal moves
        for i in range(65,73):
            if chr(i) == current_position[1]:
                continue
            if i < ord(current_position[1]):
                potential_positions['left'].append((current_position[0],chr(i)))
            else:
                potential_positions['right'].append((current_position[0],chr(i)))
        
        for direction, square in potential_positions.items():
            if tuple(endposition) in square:
                return potential_positions[direction]

class Knight(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.can_jump = True
    
    def get_unhindered_positions(self, endposition):
        current_position = self.position
        potential_positions = [
            (current_position[0]+2, chr(ord(current_position[1])+1)),
            (current_position[0]+2, chr(ord(current_position[1])-1)),
            (current_position[0]-2, chr(ord(current_position[1])+1)),
            (current_position[0]-2, chr(ord(current_position[1])+-1)),
            (current_position[0]+1, chr(ord(current_position[1])+2)),
            (current_position[0]-1, chr(ord(current_position[1])+2)),
            (current_position[0]-1, chr(ord(current_position[1])-2)),
            (current_position[0]+1, chr(ord(current_position[1])-2))
            ]
        potential_positions =[i for i in potential_positions \
            if self.pos_within_bounds(i) is True]
        
        if tuple(endposition) in potential_positions:
            return potential_positions

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
    
    def get_unhindered_positions(self, endposition):
        current_position = self.position
        potential_positions = {
                        'down' : [], 
                        'diag1' : [],
                        'diag2' : []
                        }
        potential_positions['down'] += [(current_position[0]-1, current_position[1])]
        if self.num_moves == 0:
            potential_positions['down'] += [(current_position[0]-2, current_position[1])]
        
        potential_positions['diag1'].append(
            (current_position[0]-1, \
            chr(ord(current_position[1])-1)
            ))

        potential_positions['diag1'].append(
            (current_position[0]-1, \
            chr(ord(current_position[1])+1)
            ))

        # for direction, square in potential_positions.items():
        #     if 1<=square[0]<=8:
        #         potential_positions[direction].remove(square)
        #     if 65<=ord(square[1])<=72:
        #         potential_positions[direction].remove(square)

        for direction, square in potential_positions.items():
            if tuple(endposition) in square:
                return potential_positions[direction]

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
    
    def get_unhindered_positions(self, endposition):
        current_position = self.position
        potential_positions = {
                        'up' : [], 
                        'diag1' : [],
                        'diag2' : []
                        }
        potential_positions['up'] += [(current_position[0]+1, current_position[1])]
        if self.num_moves == 0:
            potential_positions['up'] += [(current_position[0]+2, current_position[1])]
        
        for direction, square in potential_positions.items():
            if tuple(endposition) in square:
                return potential_positions[direction]

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
    king = WhiteKing(position=[1,'E'])
    rook = BlackRook(position=[3,'C'])
    queen = Queen(position=[4,'D'])
    knight = BlackKnight(position=[8,'G'])
    whitepawn = WhitePawn(position=[7,'B'])
    blackpawn = BlackPawn(position=[2,'H'])

    #test positions
    print ('\nBISHOP')
    print(bishop.get_unhindered_positions(endposition=[2,'E']))
    print(bishop.get_unhindered_positions(endposition=[3,'E']))
    
    print ('\nKING')
    print(king.get_unhindered_positions(endposition=[2,'E']))
    print(king.get_unhindered_positions(endposition=[3,'F']))

    print ('\nQUEEN')
    print(queen.get_unhindered_positions(endposition=[8,'H']))
    print(queen.get_unhindered_positions(endposition=[3,'F']))

    print ('\nROOK')
    print(rook.get_unhindered_positions(endposition=[2,'C']))
    print(rook.get_unhindered_positions(endposition=[7,'G']))

    print('\nKNIGHT')
    #print(knight.get_unhindered_positions(endposition=[8,'f']))
    print(knight.get_unhindered_positions(endposition=[6,'H']))

    print('\n WHITE PAWN')
    print(whitepawn.get_unhindered_positions(endposition=[6,'B']))
    print(whitepawn.get_unhindered_positions(endposition=[8,'E']))

    print('\n BLACK PAWN')
    print(blackpawn.get_unhindered_positions(endposition=[4,'H']))
    print(blackpawn.get_unhindered_positions(endposition=[8,'E']))