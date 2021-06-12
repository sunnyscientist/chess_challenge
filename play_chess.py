import time
from chess_board import ChessBoard
from chess_pieces import (chess_piece_acronyms, WhiteChessPiece, Pawn)

def is_valid_move(chessboard,chesspiece, endpos):
    valid_move = None
    attack = None

    if chesspiece.colour[0] == 'W':
        player = 'W'
        opponent = 'B'
    else:
        player = 'B'
        opponent = 'W'
    player_army = chessboard.get_army_location(colour = player)        
    opposition_army = chessboard.get_army_location(colour = opponent)
    potential_piece_positions = chesspiece.get_unhindered_positions(endpos)
        
    if potential_piece_positions is None:
        print('Invalid directional move for this piece')
        valid_move = False
        return valid_move, attack

    if chesspiece.can_jump is True: #knight
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


if __name__ == '__main__':
    print ('\n\nWelcome to a game of chess!')
    time.sleep(1)
    print (('\nTo configure symbols, confirm whether the following unicode'),
    ('chess characters are correctly represented\n\n'))
    
    test_symbols = [u'\u265F', u'\u265E', u'\u265C', '♚', '♕', '♝', '♘']
    print (test_symbols)
    configure_symbols = input('y/n to proceed:\t')
    if configure_symbols in ['y', 'Y', 'yes', 'YES']:
        symbol = True
    else:
        symbol = False
    print (('To move a piece type the shortened piece name, followed by '),
    ('the current position of the piece and the place where you want to move'),
    (' e.g.: \nWP A2 A4\n\n'))

    print('The acronyms for each piece are as follows: ')
    for k,v in chess_piece_acronyms.items():
        print ('{} : {}'.format(k,v))
    time.sleep(1)
    print ('\nInitialising game.... White moves first!\n')
    time.sleep(1)
    
    chessboard = ChessBoard()
    chessboard.initialise_game(piece_unicode=symbol)
    
    players = {1:'W', 2:'B'}
    player = 1
    opponent = 2

    while True:
        # log state of board (dict with turn number)
        chessboard.game_log[chessboard.turns] = chessboard.chessboard
        
        #validate command 
        chesspiece, startpos, endpos = chessboard.check_command(player=player)
        endpos = tuple(endpos)
        valid_move, attack = chessboard.is_valid_move(chesspiece,endpos)
                
        if valid_move is not True:
            print('Illegal move')
            continue

        if attack is True:
            #find piece at location
            #take it off board
            #add to relevant fallen army
            fallen_piece = chessboard.find_piece_onboard(pos = endpos, \
                colour = players[opponent] )
            fallen_piece.killed = True

            if isinstance(fallen_piece, WhiteChessPiece):
                chessboard.fallen_white_army.append(fallen_piece)
            else:
                chessboard.fallen_black_army.append(fallen_piece)
                
        chesspiece.num_moves+=1
        chesspiece.position = endpos   
        chessboard.chessboard.loc[startpos[0],startpos[1]] = None
        chessboard.update_board()
        chessboard.turns +=1
        player,opponent = opponent,player