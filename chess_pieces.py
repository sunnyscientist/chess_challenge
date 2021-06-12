class ChessPiece():
    """Generic Chess Piece"""

    def __init__(self, position, unicode=False):
        if isinstance(position, list):
            position = tuple(position)
        self.starting_position = position
        self.__position = position
        self.unicode = unicode
        self.symbols = [0, 1]
        self.num_moves = 0
        self.killed = False
        self.can_jump = False
        self.nrows = 8
        self.ncols = 8
    
    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        if isinstance(position, list):
            position = tuple(position)
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

class WhiteChessPiece(ChessPiece):
    """White Chess Piece"""
    def __init__(self, position, unicode=False):
        super().__init__(position,unicode)
        self.colour = 'WHITE'

class BlackChessPiece(ChessPiece):
    """Black Chess Piece"""

    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
        self.colour = 'BLACK'

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
                        'diag2' : [],
                        'diag3' : [],
                        'diag4' : []
                        }
        #planar moves
        space_down = current_position[0]-1
        space_up = self.ncols-current_position[0]
        space_right = self.nrows - (ord('H')-ord(current_position[1]))
        space_left = ord(current_position[1]) - ord('A')

        for i in range(1, space_down+1):
            pos = (current_position[0]-i, current_position[1])
            if self.pos_within_bounds(pos):
                potential_positions['down'].append(pos)
            diag1 = (current_position[0]-i, chr(ord(current_position[1])+i))
            diag2 = (current_position[0]-i, chr(ord(current_position[1])-i))
            if self.pos_within_bounds(diag1):
                potential_positions['diag1'].append(diag1)
            if self.pos_within_bounds(diag2):
                potential_positions['diag2'].append(diag2)

        for i in range(1, space_up+1):
            pos = (current_position[0]+i, current_position[1])
            if self.pos_within_bounds(pos):
                potential_positions['up'].append(pos)
            
            diag3 = (current_position[0]+i, chr(ord(current_position[1])+i))
            diag4 = (current_position[0]+i, chr(ord(current_position[1])-i))
            if self.pos_within_bounds(diag3):
                potential_positions['diag3'].append(diag3)
            if self.pos_within_bounds(diag4):
                potential_positions['diag4'].append(diag4)
        
        for i in range(1, space_left+1):
            pos = (current_position[0], chr(ord(current_position[1])-i))
            if self.pos_within_bounds(pos):
                potential_positions['left'].append(pos)

        for i in range(1, space_right+1):
            pos = (current_position[0], chr(ord(current_position[1])+i))
            if self.pos_within_bounds(pos):
                potential_positions['right'].append(pos)        
        
        for direction, square in potential_positions.items():
            if tuple(endposition) in square:
               return potential_positions[direction]

class King(ChessPiece):
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
                        'diag2' : [],
                        'diag3' : [],
                        'diag4' : []
                        }
        left = (current_position[0], chr(ord(current_position[1])-1))
        if self.pos_within_bounds(left):
            potential_positions['left'].append(left)

        right = (current_position[0], chr(ord(current_position[1])+1))
        if self.pos_within_bounds(right):
            potential_positions['right'].append(right)
        
        up = (current_position[0]+1, current_position[1])
        if self.pos_within_bounds(up):
            potential_positions['up'].append(up)
        
        down = (current_position[0]-1, current_position[1])
        if self.pos_within_bounds(down):
            potential_positions['down'].append(down)

        diag1 = (current_position[0]+1, chr(ord(current_position[1])+1))
        if self.pos_within_bounds(diag1):
            potential_positions['diag1'].append(diag1)
        
        diag2 = (current_position[0]+1, chr(ord(current_position[1])-1))
        if self.pos_within_bounds(diag2):
            potential_positions['diag2'].append(diag2)
        
        diag3 = (current_position[0]-1, chr(ord(current_position[1])+1))
        if self.pos_within_bounds(diag3):
            potential_positions['diag3'].append(diag3)
        
        diag4 = (current_position[0]-1, chr(ord(current_position[1])-1))
        if self.pos_within_bounds(diag4):
            potential_positions['diag4'].append(diag4)
                
        for direction, square in potential_positions.items():
            if tuple(endposition) in square:
               return potential_positions[direction]

class Bishop(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)
    
    def get_unhindered_positions(self, endposition):
        """
        Bishops can move diagonally i.e.
        the same number of squares horizontal and vertical
        """
        current_position = self.position
        potential_positions = { 
                        'diag1' : [],
                        'diag2' : [],
                        'diag3' : [],
                        'diag4' : []
                        }
        space_down = current_position[0]-1
        space_up = self.ncols-current_position[0]
        space_right = self.nrows - (ord('H')-ord(current_position[1]))
        space_left = ord(current_position[1]) - ord('A')

        for i in range(1, space_down+1):
            diag1 = (current_position[0]-i, chr(ord(current_position[1])+i))
            diag2 = (current_position[0]-i, chr(ord(current_position[1])-i))
            if self.pos_within_bounds(diag1):
                potential_positions['diag1'].append(diag1)
            if self.pos_within_bounds(diag2):
                potential_positions['diag2'].append(diag2)

        for i in range(1, space_up+1):
            diag3 = (current_position[0]+i, chr(ord(current_position[1])+i))
            diag4 = (current_position[0]+i, chr(ord(current_position[1])-i))
            if self.pos_within_bounds(diag3):
                potential_positions['diag3'].append(diag3)
            if self.pos_within_bounds(diag4):
                potential_positions['diag4'].append(diag4)
        
        for direction, square in potential_positions.items():
            if tuple(endposition) in square:
                return potential_positions[direction]

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
        space_down = current_position[0]-1
        space_up = self.ncols-current_position[0]
        space_right = self.nrows - (ord('H')-ord(current_position[1]))
        space_left = ord(current_position[1]) - ord('A')

        for i in range(1, space_down+1):
            pos = (current_position[0]-i, current_position[1])
            if self.pos_within_bounds(pos):
                potential_positions['down'].append(pos)

        for i in range(1, space_up+1):
            pos = (current_position[0]+i, current_position[1])
            if self.pos_within_bounds(pos):
                potential_positions['up'].append(pos)
        
        for i in range(1, space_left+1):
            pos = (current_position[0], chr(ord(current_position[1])-i))
            if self.pos_within_bounds(pos):
                potential_positions['left'].append(pos)

        for i in range(1, space_right+1):
            pos = (current_position[0], chr(ord(current_position[1])+i))
            if self.pos_within_bounds(pos):
                potential_positions['right'].append(pos)

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
        self.diagonal_move = None

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
        
        diag1 = (current_position[0]-1, chr(ord(current_position[1])+1))
        if self.pos_within_bounds(diag1):
            potential_positions['diag1'].append(diag1)
        
        diag2 = (current_position[0]-1, chr(ord(current_position[1])-1))
        if self.pos_within_bounds(diag2):
            potential_positions['diag2'].append(diag2)

        for direction, square in potential_positions.items():
            if tuple(endposition) in square:
                if direction in ['diag1', 'diag2']:
                    self.diagonal_move = True
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
        
        diag1 = (current_position[0]+1, chr(ord(current_position[1])+1))
        if self.pos_within_bounds(diag1):
            potential_positions['diag1'].append(diag1)
        
        diag2 = (current_position[0]+1, chr(ord(current_position[1])-1))
        if self.pos_within_bounds(diag2):
            potential_positions['diag2'].append(diag2)
        
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