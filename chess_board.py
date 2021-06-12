import pandas as pd
from tabulate import tabulate

from chess_pieces import (ChessPiece, WhiteKing, WhiteQueen, Pawn,
WhiteBishop, WhiteKnight, WhiteRook, WhitePawn, BlackKing, BlackQueen, 
BlackBishop, BlackKnight, BlackRook, BlackPawn, map_text_piece)

class ChessBoard():
    def __init__(self):
        self.init_board()
        self.turns = 0
        self.game_log = {}
        self.fallen_white_army = []
        self.fallen_black_army = []

    def init_board(self):

        self.cols = [chr(i) for i in range(65,73)]
        self.rows = [i for i in range(8,0,-1)]
        board_values = [[None] * len(self.cols) for i in range(len(self.rows))]
        self.chessboard = pd.DataFrame(data=board_values, columns=self.cols, \
            index=self.rows)

    def print_chessboard(self):
        printed_chessboard = tabulate(self.chessboard, headers= self.cols, 
        showindex='always', tablefmt="fancy_grid", colalign=("center",))
        print('\n===========================================================')
        if len(self.fallen_black_army) >0:
            print(f'\nFallen Black Pieces: {self.fallen_black_army}\n')
        print('\n')
        print(printed_chessboard)
        print('\n')
        if len(self.fallen_white_army) >0:
            print(f'\nFallen White Pieces: {self.fallen_white_army}\n')
        print('===========================================================')

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
        self.chess_set = self.white_army + self.black_army

        for setpiece in self.chess_set:
            if isinstance(setpiece, list):
                for piece in setpiece:
                    self.chessboard.loc[piece.position[0], piece.position[1]] \
                        = piece
            else:
                self.chessboard.loc[setpiece.position[0], \
                    setpiece.position[1]] = setpiece
        
        self.print_chessboard()
    
    def get_army_location(self, colour):
        army_location = []
        for setpiece in self.army_map[colour]:
            if isinstance(setpiece, list):
                for piece in setpiece:
                    if piece.killed is False:
                        army_location.append(tuple(piece.position))
            else:
                if setpiece.killed is False:
                        army_location.append(tuple(setpiece.position))
        return army_location
        
    def check_command(self, player):
        """
        Checks syntax of move command
        """ 
        command_success = []
        while True:     
            try:
                command = input('Player {} - Enter move:\t'.format(player))  
                piece, start_pos, end_pos = command.split()
                start_pos = start_pos.upper()
                end_pos = end_pos.upper()

                #find invalid commands
                if piece not in map_text_piece.keys():
                    raise Exception( 'Invalid Acronym for Piece!')
                if len(start_pos)!=2 or len(end_pos)!=2:
                    raise Exception('Piece position not in valid format')
                if start_pos == end_pos:
                    raise('End position cannot be the same as the start')
                
                if piece[0] != 'W' and self.turns == 0:
                    raise Exception('For the first turn, white moves first')
                elif piece[0] == 'W' and self.turns%2==1:
                    raise Exception('Black Piece to Move')
                elif piece[0] == 'B' and self.turns%2==0:
                    raise Exception('White Piece to Move')
                
                #correct ordering of grid position if necessary
                if start_pos[0].isdigit() and start_pos[1].isalpha():
                    correct_start_pos = (int(start_pos[0]), start_pos[1])
                elif start_pos[1].isdigit() and start_pos[0].isalpha():
                    correct_start_pos = (int(start_pos[1]), start_pos[0])
                else:
                    raise Exception((('Board Position must be composed of a '),
                    ('letter and number')))
                
                if end_pos[0].isdigit() and end_pos[1].isalpha():
                    correct_end_pos = (int(end_pos[0]), end_pos[1])
                elif end_pos[1].isdigit() and end_pos[0].isalpha():
                    correct_end_pos = (int(end_pos[1]), end_pos[0])
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
                
                self.piece_in_play = self.find_piece_onboard(pos=correct_start_pos,\
                    colour=piece[0])

            except Exception as e:
                print('ERROR: {}\n'.format(e))
                print ('Please try again.\n')
            else:
                command_success.append(self.piece_in_play)
                command_success.append(correct_start_pos)
                command_success.append(correct_end_pos)
                break
        return command_success

    def update_board(self):
        for setpiece in self.chess_set:
            if isinstance(setpiece, list):
                for piece in setpiece:
                    if piece.killed is False:
                        self.chessboard.loc[piece.position[0], \
                            piece.position[1]] = piece
            else:
                if setpiece.killed is False:
                    self.chessboard.loc[setpiece.position[0], \
                    setpiece.position[1]] = setpiece
        self.print_chessboard()

    def find_piece_onboard(self, pos, colour):

        if isinstance(pos, tuple):
            pos = list(pos)
        if type(pos[0]) != int:
            pos[0],pos[1] = pos[1],pos[0]
        pos = tuple(pos)

        for setpiece in self.army_map[colour]:
            if isinstance(setpiece, list):
                for piece in setpiece:
                    if piece.position == pos:
                        return piece
            else:
                if setpiece.position == pos:
                    return setpiece
    
    def is_valid_move(self,chesspiece, endpos):
        valid_move = None
        attack = None

        if chesspiece.colour[0] == 'W':
            player = 'W'
            opponent = 'B'
        else:
            player = 'B'
            opponent = 'W'
        player_army = self.get_army_location(colour = player)        
        opposition_army = self.get_army_location(colour = opponent)
        potential_piece_positions = chesspiece.get_unhindered_positions(endpos)
            
        if potential_piece_positions is None:
            print('Invalid directional move for this piece')
            valid_move = False
            return valid_move, attack

        if chesspiece.can_jump is True: # only knight
            if endpos in potential_piece_positions:
                if endpos in opposition_army:
                    valid_move = True
                    attack = True
                elif endpos in player_army:
                    valid_move = False
                else:
                    valid_move = True
            else:
                valid_move = False
        elif isinstance(chesspiece, Pawn) and chesspiece.diagonal_move is True:
            if endpos in opposition_army:
                    valid_move = True
                    attack = True
            else:
                print('Pawn can only move diagonally if opponent is present.')
                valid_move=False
            chesspiece.diagonal_move = None #reset for next move
        elif isinstance(chesspiece, Pawn) and chesspiece.diagonal_move is not True:
            if endpos in opposition_army or endpos in player_army:
                    valid_move = False
            else:
                valid_move=True
        else:
            position_idx = potential_piece_positions.index(endpos)
            #iterate through in order of movement to check if any obstructions
            for i in range(position_idx+1):
                if potential_piece_positions[i] in opposition_army or \
                    potential_piece_positions[i] in player_army:
                    if i < position_idx:
                        valid_move = False
                        break
                    elif i == position_idx and \
                        potential_piece_positions[i] in opposition_army:
                        valid_move = True
                        attack = True
                    elif i == position_idx and \
                        potential_piece_positions[i] in player_army:
                        valid_move = False
            
            if valid_move is None:
                valid_move = True
                            
        return valid_move, attack
    # def in_check(self, colour):
    #     if colour == 'W':
    #         for setpiece in self.black_army:
    #             if isinstance(setpiece, list):
    #                 for piece in setpiece:
    #                     if piece.killed is True:
    #                         continue
    #                         return piece
    #         else:
    #             if setpiece.position == pos:
    #                 return setpiece
if __name__ == '__main__':
    chessboard = ChessBoard()