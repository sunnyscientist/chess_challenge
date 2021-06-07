import pandas as pd
from colorama import Back
from tabulate import tabulate

from chess_pieces import (WhiteKing, WhiteQueen, WhiteBishop, 
WhiteKnight, WhiteRook, WhitePawn, BlackKing, BlackQueen, BlackBishop,
BlackKnight, BlackRook, BlackPawn)

class ChessBoard():
    def __init__(self):
        self.draw_board()

    def draw_board(self):

        self.cols = [chr(i) for i in range(65,73)]
        self.rows = [i for i in range(8,0,-1)]
        board_values = [[None] * len(self.cols) for i in range(len(self.rows))]
        self.chessboard = pd.DataFrame(data=board_values, columns=self.cols, \
            index=self.rows)

    def print_chessboard(self):
        printed_chessboard = tabulate(self.chessboard, headers= self.cols, 
        showindex='always', tablefmt="fancy_grid", colalign=("center",))
        print(printed_chessboard)

    def initialise_game(self, piece_unicode=False):

        # white pieces
        white_queen = WhiteQueen(position=[8,'D'], unicode=piece_unicode)
        white_king = WhiteKing(position=[8,'E'], unicode=piece_unicode)
        white_bishops = [WhiteBishop(position=[8,'C'], unicode=piece_unicode), 
                        WhiteBishop(position=[8,'F'], unicode=piece_unicode)]
        white_knights = [WhiteKnight(position=[8,'B'], unicode=piece_unicode),
                        WhiteKnight(position=[8,'G'], unicode=piece_unicode)]
        white_rooks = [WhiteRook(position=[8,'A'], unicode=piece_unicode),
                    WhiteRook(position=[8,'H'], unicode=piece_unicode)]
        white_pawns = [WhitePawn(position=[7,i], unicode=piece_unicode) \
            for i in self.chessboard.columns]

        # black pieces
        black_queen = BlackQueen(position=[1,'D'], unicode=piece_unicode)
        black_king = BlackKing(position=[1,'E'], unicode=piece_unicode)
        black_bishops = [BlackBishop(position=[1,'C'], unicode=piece_unicode), 
                        BlackBishop(position=[1,'F'], unicode=piece_unicode)]
        black_knights = [BlackKnight(position=[1,'B'], unicode=piece_unicode),
                        BlackKnight(position=[1,'G'], unicode=piece_unicode)]
        black_rooks = [BlackRook(position=[1,'A'], unicode=piece_unicode),
                    BlackRook(position=[1,'H'], unicode=piece_unicode)]
        black_pawns = [BlackPawn(position=[2,i], unicode=piece_unicode) \
            for i in self.chessboard.columns]
        
        chess_set = [white_queen, white_king, white_bishops, white_knights,
        white_rooks, white_pawns, black_queen, black_king, black_bishops,
        black_knights, black_rooks, black_pawns]

        for setpiece in chess_set:
            if isinstance(setpiece, list):
                for piece in setpiece:
                    self.chessboard.loc[piece.position[0], piece.position[1]] = piece
            else:
                self.chessboard.loc[setpiece.position[0], setpiece.position[1]] = setpiece      
        
        self.print_chessboard()
    
    def apply_board_colours(self):
        # TODO: style board
        pass
        # background_colours = [Back.RED, Back.YELLOW]
        # for i in range(len(self.chessboard)):
        #     for j in range(len(self.chessboard)):
                
        #         if i == j:
        #             square_colour = background_colours[1]
        #         elif i%2==1 and j%2==0:
        #             square_colour = background_colours[0]
        #         elif i%2==0 and j%2==1:
        #             square_colour = background_colours[1]
        #         # else:
        #         #     square_colour = background_colours[0]
        #         self.chessboard[i][j] = f"{square_colour}"


if __name__ == '__main__':
    chessboard = ChessBoard()