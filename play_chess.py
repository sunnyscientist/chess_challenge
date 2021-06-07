import time
from chess_board import ChessBoard
from chess_pieces import chess_piece_acronyms

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
    
    players = [1,2]
    player = players[0]

    while True:
        # check command syntax
        chesspiece, startpos, end_pos = chessboard.check_command(player=player)
        chessboard.remove_invalid_moves(chesspiece, startpos)
        # check move is valid
        # check if opponent in way
        # if valid move/take piece
            #add one to turns
            # log state of board
            #switch players
        # else retry until successful command
        
        break