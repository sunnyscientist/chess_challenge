import os
import sys
import time
sys.path.insert(0,os.path.abspath('..'))
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
        chessboard.print_chessboard()
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
                print('die')
            else:
                chessboard.fallen_black_army.append(fallen_piece)
                print('dead')
                
        chesspiece.num_moves+=1
        chesspiece.position = endpos   
        chessboard.chessboard.loc[startpos[0],startpos[1]] = None
        chessboard.update_board()
        chessboard.turns +=1
        player,opponent = opponent,player