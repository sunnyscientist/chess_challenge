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
    
    players = {1:'W', 2:'B'}
    player = 1
    opponent = 2

    while True:
        # check command syntax
        chesspiece, startpos, endpos = chessboard.check_command(player=player)
        endpos = tuple(endpos)
        print (chesspiece, startpos, endpos)
        army_map = chessboard.get_army_location(colour= players[player])        
        opposition_army = chessboard.get_army_location(colour= players[opponent])
        potential_piece_positions = chesspiece.get_unhindered_positions(endpos)
        print (potential_piece_positions)
        print (endpos)
        #remove squares occupied by own side
        for pos in potential_piece_positions:
            if pos in army_map:
                potential_piece_positions.remove(pos)
        if len(potential_piece_positions) == 0:
            print('Invalid move: One of your pieces occupies this space')
            continue

        attack = None
        valid_move = None
        # TODO: FIGURE OUT PIECE MOVEMENTS SPECIFICALLY
        # all pieces apart from knight can't jump
        if chesspiece.can_jump is True: #knight
            if endpos in potential_piece_positions:
                valid_move = True
                if endpos in opposition_army:
                    attack = True
                else:
                    attack = False
            else:
                valid_move = False
                attack = False
        else:
            #iterate through in order of movement to check if any obstructions
            pass
        print (valid_move)
        if valid_move is not True:
            continue
        print (chesspiece.position)
        chessboard.chessboard.loc[startpos[0],startpos[1]] = None
        chesspiece.position = endpos
        print (chesspiece.position)
        chessboard.update_board()
        chessboard.turns +=1
        player,opponent = opponent,player
        print (player)
        # log state of board (dict with turn number)
        # if attack is true mark fallen piece
        # take fallen piece of board
        # redraw board
        # add one to turns
        # switch player 






        
        # check move is valid
        # check if opponent in way
        # CHECK IF END POS HAD OPPOINENT PIECE
        # if valid move/take piece
            #add one to turns
            # log state of board
            #switch players
        # else retry until successful command
        
        break

""" CREATE DICTINARIES OF POTENTIAL MOVES
EG QUEEN {DIAG/HORIZONTAL[]/ VERTICAL}
ITERATE THROUGH IN ORDER
IF OPPENENT PIECE EXISTS REMOVE FOLLOWING FROM UNHINDERED
PAWNS- CHECK FORWARD DIAGONAL ONLY IF OPPONENT
KNIGHT CAN JUMP OVER PICE
"""