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
        self.white_queen = WhiteQueen(position=[8,'D'], unicode=piece_unicode)
        self.white_king = WhiteKing(position=[8,'E'], unicode=piece_unicode)
        self.white_bishops = [WhiteBishop(position=[8,'C'], unicode=piece_unicode), 
                        WhiteBishop(position=[8,'F'], unicode=piece_unicode)]
        self.white_knights = [WhiteKnight(position=[8,'B'], unicode=piece_unicode),
                        WhiteKnight(position=[8,'G'], unicode=piece_unicode)]
        self.white_rooks = [WhiteRook(position=[8,'A'], unicode=piece_unicode),
                    WhiteRook(position=[8,'H'], unicode=piece_unicode)]
        self.white_pawns = [WhitePawn(position=[7,i], unicode=piece_unicode) \
            for i in self.chessboard.columns]

        # black pieces
        self.black_queen = BlackQueen(position=[1,'D'], unicode=piece_unicode)
        self.black_king = BlackKing(position=[1,'E'], unicode=piece_unicode)
        self.black_bishops = [BlackBishop(position=[1,'C'], unicode=piece_unicode), 
                        BlackBishop(position=[1,'F'], unicode=piece_unicode)]
        self.black_knights = [BlackKnight(position=[1,'B'], unicode=piece_unicode),
                        BlackKnight(position=[1,'G'], unicode=piece_unicode)]
        self.black_rooks = [BlackRook(position=[1,'A'], unicode=piece_unicode),
                    BlackRook(position=[1,'H'], unicode=piece_unicode)]
        self.black_pawns = [BlackPawn(position=[2,i], unicode=piece_unicode) \
            for i in self.chessboard.columns]
        
        self.white_army = [self.white_queen, self.white_king, \
            self.white_bishops, self.white_knights, self.white_rooks, \
            self.white_pawns]
        
        self.black_army = [self.black_queen, self.black_king, \
            self.black_bishops, self.black_knights, self.black_rooks, \
            self.black_pawns]

        self.army_map = {'W': self.white_army, 'B' : self.black_army}
        chess_set = self.white_army + self.black_army

        for setpiece in chess_set:
            if isinstance(setpiece, list):
                for piece in setpiece:
                    self.chessboard.loc[piece.position[0], piece.position[1]] \
                        = piece
            else:
                self.chessboard.loc[setpiece.position[0], \
                    setpiece.position[1]] = setpiece
        
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

                # check piece is at starting position
                if not isinstance(self.chessboard.loc[correct_start_pos[0], \
                    correct_start_pos[1]], map_text_piece[piece]):
                    raise Exception('{} does not exist at {}'.format(piece, \
                        correct_start_pos))
                
                piece_in_play = None
                for setpiece in self.army_map[piece[0]]:
                    if isinstance(setpiece, list):
                        for piece in setpiece:
                            if piece.position == correct_start_pos:
                                piece_in_play = piece
                    else:
                        if setpiece.position == correct_start_pos:
                                piece_in_play = setpiece

            except Exception as e:
                print('ERROR: {}\n'.format(e))
                print ('Please try again.\n')
            else:
                command_success.append(piece_in_play)
                command_success.append(correct_start_pos)
                command_success.append(correct_end_pos)
                break
        return command_success

    # def get_army_state(self, colour):
    #     army_location = []
    #     for setpiece in self.army_map[colour]:
    #         if isinstance(setpiece, list):
    #             for piece in setpiece:
    #                 if piece.killed is False:
    #                     army_location.append(tuple(piece.position))
    #         else:
    #             if setpiece.killed is False:
    #                     army_location.append(tuple(setpiece.position))
    #     return army_location

if __name__ == '__main__':
    chessboard = ChessBoard()