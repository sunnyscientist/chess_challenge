import os
import sys
import time
sys.path.insert(0, os.path.abspath('..'))
from chess_board import ChessBoard
from chess_pieces import (chess_piece_acronyms, WhiteChessPiece, Pawn)

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
        print (f'MOVE: {chessboard.turns}\n')
        chessboard.print_chessboard()
        board_state = chessboard.chessboard.copy(deep=True)
        if chessboard.turns not in chessboard.game_log.keys():
            chessboard.game_log.update({chessboard.turns:board_state})
        #validate command 
        chesspiece, startpos, endpos = chessboard.check_command(player=player)
        endpos = tuple(endpos)

        valid_move, attack = chessboard.is_valid_move(chesspiece,endpos)
        if valid_move is not True:
            print('Illegal move')
            continue
        
        if attack is True:
            fallen_piece = chessboard.find_piece_onboard(pos = endpos, \
                colour = players[opponent] )
            fallen_piece.killed = True

            if fallen_piece.colour == 'WHITE':
                chessboard.fallen_white_army.append(fallen_piece)
            else:
                chessboard.fallen_black_army.append(fallen_piece)
        
        chesspiece.num_moves+=1
        chesspiece.position = endpos   
        chessboard.chessboard.loc[startpos[0],startpos[1]] = None
        chessboard.update_board()

        player_in_check = chessboard.in_check(players[player])
        if player_in_check is not None:
            print('Playing this move will put you in check from:')
            for piece in player_in_check[1]:
                print(f'{chess_piece_acronyms[piece.symbols[0]]} at',
                f'{piece.position[1]}{piece.position[0]}')
            print ('Please try again.\n')

            chessboard.reset_board(turn_num=chessboard.turns)
            chesspiece.position = startpos
            chessboard.chessboard.loc[endpos[0],endpos[1]] = None
            chessboard.update_board()
            continue

        opponent_in_check = chessboard.in_check(players[opponent])
        if opponent_in_check is not None:
            print(f'\nWarning:{chess_piece_acronyms[chesspiece.symbols[0]]} at',
            f'{chesspiece.position[1]}{chesspiece.position[0]} checks ',
            f'Player {opponent}')
            
            checkmate = chessboard.is_checkmate(players[opponent])
            print(checkmate)
            if checkmate is True:
                chessboard.print_chessboard()
                print (f'\n\nCHECKMATE - Player {player} has won the game!')
                sys.exit()

        chessboard.turns +=1
        player,opponent = opponent,player