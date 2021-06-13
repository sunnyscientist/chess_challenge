import os
import sys
import pandas as pd
from tabulate import tabulate
sys.path.insert(0, os.path.abspath('..'))

from chess_challenge.chess_pieces import (ChessPiece, WhiteKing, WhiteQueen, Pawn,
WhiteBishop, WhiteKnight, WhiteRook, WhitePawn, BlackKing, BlackQueen, 
BlackBishop, BlackKnight, BlackRook, BlackPawn, map_text_piece)

class ChessBoard():
    def __init__(self):
        self.init_board()
        self.turns = 0
        self.game_log = {}
        self.fallen_white_army = []
        self.fallen_black_army = []

    def init_board(self, board_values=None):
        """Initialise board with None values"""

        self.cols = [chr(i) for i in range(65,73)]
        self.rows = [i for i in range(8,0,-1)]
        if board_values is not None:
            try:
                self.chessboard = pd.DataFrame(data=board_values, \
                columns=self.cols,index=self.rows)
            except Exception:
                board_values = [[None] * len(self.cols) for i in range(len(self.rows))]
                self.chessboard = pd.DataFrame(data=board_values, \
                columns=self.cols,index=self.rows)
        else:
            board_values = [[None] * len(self.cols) for i in range(len(self.rows))]
            self.chessboard = pd.DataFrame(data=board_values, \
                columns=self.cols,index=self.rows)

    def print_chessboard(self):
        """Method to display chessboard"""

        printed_chessboard = tabulate(self.chessboard, headers= self.cols, 
        showindex='always', tablefmt="fancy_grid", colalign=("center",))
        print('\n===========================================================')
        if len(self.fallen_white_army) >0:
            print(f'\nFallen White Pieces: {self.fallen_white_army}\n')
        print('\n')
        print(printed_chessboard)
        print('\n')
        if len(self.fallen_black_army) >0:
            print(f'\nFallen Black Pieces: {self.fallen_black_army}\n')
        print('===========================================================')

    def initialise_game(self, piece_unicode=False):
        """
        Initialises board with starting positions of pieces
        """
        # white pieces
        self.white_queen = WhiteQueen(position=[1,'D'], unicode=piece_unicode)
        self.white_king = WhiteKing(position=[1,'E'], unicode=piece_unicode)
        self.white_bishops = [WhiteBishop(position=[1,'C'], unicode=piece_unicode), 
                        WhiteBishop(position=[1,'F'], unicode=piece_unicode)]
        self.white_knights = [WhiteKnight(position=[1,'B'], unicode=piece_unicode),
                        WhiteKnight(position=[1,'G'], unicode=piece_unicode)]
        self.white_rooks = [WhiteRook(position=[1,'A'], unicode=piece_unicode),
                    WhiteRook(position=[1,'H'], unicode=piece_unicode)]
        self.white_pawns = [WhitePawn(position=[2,i], unicode=piece_unicode) \
            for i in self.chessboard.columns]

        # black pieces
        self.black_queen = BlackQueen(position=[8,'D'], unicode=piece_unicode)
        self.black_king = BlackKing(position=[8,'E'], unicode=piece_unicode)
        self.black_bishops = [BlackBishop(position=[8,'C'], unicode=piece_unicode), 
                        BlackBishop(position=[8,'F'], unicode=piece_unicode)]
        self.black_knights = [BlackKnight(position=[8,'B'], unicode=piece_unicode),
                        BlackKnight(position=[8,'G'], unicode=piece_unicode)]
        self.black_rooks = [BlackRook(position=[8,'A'], unicode=piece_unicode),
                    BlackRook(position=[8,'H'], unicode=piece_unicode)]
        self.black_pawns = [BlackPawn(position=[7,i], unicode=piece_unicode) \
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
    
    def get_army_location(self, colour):
        """Returns a list of positions that an specific side occupies"""
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
        """Updates board positions based on pieces"""
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

    def find_piece_onboard(self, pos, colour):
        """Method to find specific ChessPiece Instance from position"""

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
        """Checks the legality of a chesspiece and its desired destination"""
        valid_move = None
        attack = None

        if isinstance(endpos, tuple):
            endpos = list(endpos)
        if type(endpos[0]) != int:
            endpos[0],endpos[1] = endpos[1],endpos[0]
        endpos = tuple(endpos)

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
        elif isinstance(chesspiece, Pawn): #only pawns can move diagonally
            if chesspiece.diagonal_move is True:
                if endpos in opposition_army:
                        valid_move = True
                        attack = True
                else:
                    valid_move=False
            else: #pawns cannot take opponent pieces directly in front
                if endpos in opposition_army or endpos in player_army:
                    valid_move = False
                else:
                    valid_move=True
            chesspiece.diagonal_move = None #reset for next move   
        else:
            position_idx = potential_piece_positions.index(endpos)
            #iterate through in order of movement to check if any obstructions
            for i in range(position_idx+1):
                if potential_piece_positions[i] in opposition_army or \
                    potential_piece_positions[i] in player_army:
                    #piece in the way that you can't jump over
                    if i < position_idx:
                        valid_move = False
                        break
                    #valid attack move
                    elif i == position_idx and \
                        potential_piece_positions[i] in opposition_army:
                        valid_move = True
                        attack = True
                    #own piece occupying square
                    elif i == position_idx and \
                        potential_piece_positions[i] in player_army:
                        valid_move = False
            
            if valid_move is None:
                valid_move = True
                            
        return valid_move, attack
    
    def in_check(self, colour):
        """Method to detect whether a king is in check"""

        if colour == 'W':
            opposition = self.black_army
            king = self.white_king
        else:
            opposition = self.white_army
            king = self.black_king
        
        check_pieces = []
        #check if king is in available moves for opponent
        for setpiece in opposition:
            if isinstance(setpiece, list):
                for piece in setpiece:
                    available_moves = piece.get_unhindered_positions(\
                        (king.position[0],king.position[1]))
                    if available_moves is not None:
                        legal_move, attack = self.is_valid_move( \
                            piece, (king.position[0],king.position[1]))
                        if (legal_move, attack) == (True, True):
                            check_pieces.append(piece)
            else:
                available_moves = setpiece.get_unhindered_positions( \
                    (king.position[0],king.position[1]))
                if available_moves is not None:
                        legal_move, attack = self.is_valid_move( \
                            setpiece, (king.position[0],king.position[1]))
                        if (legal_move, attack) == (True, True):
                            check_pieces.append(setpiece)
        if len(check_pieces)>0:
            return True, check_pieces
    
    def is_checkmate(self,colour):
        """Method to determine whether checkmate has occured"""
        if colour == 'W':
            opposition = self.black_army
            king = self.white_king
        else:
            opposition = self.white_army
            king = self.black_king
        potential_moves = king.get_unhindered_positions().values()
        possible_moves = [move for sublist in potential_moves for move in sublist]
        
        # king can only move max of 8 positions. if each position is covered
        # by an attacker it is checkmate
        attacking_squares = 0
        for move in possible_moves:
            for setpiece in opposition:
                if isinstance(setpiece, list):
                    for piece in setpiece:
                        potential_attack = piece.get_unhindered_positions(move)
                        valid_move, attack = self.is_valid_move(piece, move)
                        if valid_move is False:
                            attacking_squares +=1
                            break
                        elif valid_move is True and attack is True:
                            attacking_squares += 1
                            break
                else:
                    potential_attack = setpiece.get_unhindered_positions(move)
                    valid_move, attack = self.is_valid_move(setpiece, move)
                    if valid_move is False:
                        attacking_squares +=1
                        break
                    elif valid_move is True and attack is True:
                        attacking_squares += 1
                        break

        if attacking_squares == len(possible_moves):
            checkmate = True
        else:
            checkmate = False
        return checkmate
  
    def reset_board(self, turn_num):
        """Resets board for a specific turn"""
        self.init_board(board_values=self.game_log[turn_num])
        white_rook_counter = 0
        white_bishop_counter = 0
        white_knight_counter = 0
        white_pawn_counter = 0
        black_rook_counter = 0
        black_bishop_counter = 0
        black_knight_counter = 0
        black_pawn_counter = 0

        for column in self.chessboard.columns:
            for i in range(1,9):
                if self.chessboard.loc[i,column] == None:
                    continue
                if isinstance(self.chessboard.loc[i,column],WhiteQueen):
                    self.white_queen.position = (i,column)
                elif isinstance(self.chessboard.loc[i,column],WhiteKing):
                    self.white_king.position = (i,column)
                elif isinstance(self.chessboard.loc[i,column],WhiteRook):
                    self.white_rooks[white_rook_counter].position = (i,column)
                    white_rook_counter +=1
                elif isinstance(self.chessboard.loc[i,column],WhiteBishop):
                    self.white_bishops[white_bishop_counter].position = (i,column)
                    white_bishop_counter += 1
                elif isinstance(self.chessboard.loc[i,column], WhitePawn):
                    self.white_pawns[white_pawn_counter].position = (i,column)
                    white_pawn_counter += 1
                elif isinstance(self.chessboard.loc[i,column], WhiteKnight):
                    self.white_knights[white_knight_counter].position = (i,column)
                    white_knight_counter += 1
                
                elif isinstance(self.chessboard.loc[i,column],BlackQueen):
                    self.black_queen.position = (i,column)
                elif isinstance(self.chessboard.loc[i,column],BlackKing):
                    self.black_king.position = (i,column)
                elif isinstance(self.chessboard.loc[i,column],BlackRook):
                    self.black_rooks[black_rook_counter].position = (i,column)
                    black_rook_counter +=1
                elif isinstance(self.chessboard.loc[i,column],BlackBishop):
                    self.black_bishops[black_bishop_counter].position = (i,column)
                    black_bishop_counter += 1
                elif isinstance(self.chessboard.loc[i,column], BlackPawn):
                    self.black_pawns[black_pawn_counter].position = (i,column)
                    black_pawn_counter += 1
                elif isinstance(self.chessboard.loc[i,column], BlackKnight):
                    self.black_knights[black_knight_counter].position = (i,column)
                    black_knight_counter += 1             

if __name__ == '__main__':
    chessboard = ChessBoard()