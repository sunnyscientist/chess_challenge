class ChessPiece():
    """Generic Chess Piece"""

    def __init__(self, position, unicode=False):
        self.__position = position
        self.unicode = unicode
        self.symbols = [0, 1]
    
    @property
    def position(self):
        return self.__position
    
    def __repr__(self):
        if self.unicode is True:
            return "{}".format(self.symbols[1])
        else:
            return "{}".format(self.symbols[0])


    #TODO: implement counter to keep track of how many moves
    #TODO: log historical locations

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

class King(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)

class Bishop(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)

class Rook(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)

class Knight(ChessPiece):
    def __init__(self, position, unicode=False):
        super().__init__(position, unicode)

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

if __name__ == '__main__':
    blackpawn = BlackPawn([1,1], unicode=False)
    print(blackpawn)
    chrs = {
    'b_checker': u'\u25FB',
    'w_checker': u'\u25FC',
}