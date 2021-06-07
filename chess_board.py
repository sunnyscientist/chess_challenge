import pandas as pd
from colorama import Back
from tabulate import tabulate

from chess_pieces import (ChessPiece, WhiteKing, WhiteQueen, WhiteBishop, 
WhiteKnight, WhiteRook, WhitePawn, BlackKing, BlackQueen, BlackBishop,
BlackKnight, BlackRook, BlackPawn, map_text_piece)

class ChessBoard():
    def __init__(self):
        self.draw_board()
        self.turns = 0

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
        """
        Initialises board with starting positions of pieces
        """
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
                    self.chessboard.loc[piece.position[0], piece.position[1]] \
                        = piece
            else:
                self.chessboard.loc[setpiece.position[0], \
                    setpiece.position[1]] = setpiece

        self.white_army = [white_queen, white_king, white_bishops,\
            white_knights, white_rooks, white_pawns]  
        self.black_army = [black_queen, black_king, black_bishops,\
            black_knights, black_rooks, black_pawns]
        
        self.print_chessboard()
    
    def check_command(self, player):
        """
        Checks syntax of move command
        """ 
        command_success = []
        while True:     
            try:
                command = input('Player {} - Enter move:\t'.format(player))  
                piece, start_pos, end_pos = command.split()

                #find invalid commands
                if piece not in map_text_piece.keys():
                    raise Exception( 'Invalid Acronym for Piece!')
                if len(start_pos)!=2 or len(end_pos)!=2:
                    raise Exception('Piece position not in valid format')
                if piece[0] != 'W' and self.turns == 0:
                    raise Exception('For the first turn, white moves first')
                
                #correct ordering of grid position if necessary
                if start_pos[0].isdigit() and start_pos[1].isalpha():
                    correct_start_pos = [int(start_pos[0]), start_pos[1]]
                elif start_pos[1].isdigit() and start_pos[0].isalpha():
                    correct_start_pos = [int(start_pos[1]), start_pos[0]]
                else:
                    raise Exception((('Board Position must be composed of a '),
                    ('letter and number')))
                
                if end_pos[0].isdigit() and end_pos[1].isalpha():
                    correct_end_pos = [int(end_pos[0]), end_pos[1]]
                elif end_pos[1].isdigit() and end_pos[0].isalpha():
                    correct_end_pos = [int(end_pos[1]), end_pos[0]]
                else:
                    raise Exception((('Board Position must be composed of a '),
                    ('letter and number')))
                
                #make sure positions within board bounds
                if correct_end_pos[1] not in self.cols or \
                    correct_start_pos[1] not in self.cols:
                    raise Exception('Board is bounded between A-H/1-8 inclusive')
                if correct_end_pos[0] not in self.rows or \
                    correct_start_pos[0] not in self.rows:
                    raise Exception('Board is bounded between A-H/1-8 inclusive')

                # TODO: check piece is at starting position

            except Exception as e:
                print('ERROR: {}\n'.format(e))
                print ('Please try again.\n')
            else:
                command_success.append(map_text_piece[piece])
                command_success.append(correct_start_pos)
                command_success.append(correct_end_pos)
                break
        return command_success
    
    def remove_invalid_moves(self, chesspiece, startpos):
        unhindered_moves = ChessPiece(position=startpos).get_unhindered_positions()
        print(unhindered_moves)
    
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