import time
from chess_board import ChessBoard
from chess_pieces import chess_piece_acronyms, WhiteChessPiece

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
        print (chesspiece, startpos, endpos)
        #get legal moves
        player_army = chessboard.get_army_location(colour= players[player])        
        opposition_army = chessboard.get_army_location(colour= players[opponent])
        potential_piece_positions = chesspiece.get_unhindered_positions(endpos)
        
        if potential_piece_positions is None:
            print('Invalid directional move for this piece')
            continue
        
        attack = None
        valid_move = None
        # TODO: FIGURE OUT PAWN MOVEMENT
        # all pieces apart from knight can't jump
        if chesspiece.can_jump is True: #knight
            if endpos in potential_piece_positions:
                if endpos in opposition_army:
                    valid_move = True
                    attack = True
                elif endpos in player_army:
                    valid_move = False
                    attack = False
                else:
                    valid_move = True
                    attack = False
            else:
                valid_move = False
                attack = False
        else:
            position_idx = potential_piece_positions.index(endpos)
            #iterate through in order of movement to check if any obstructions
            for i in range(position_idx+1):
                if potential_piece_positions[i] in opposition_army or \
                    potential_piece_positions[i] in player_army:
                    if i < position_idx:
                        valid_move = False
                    elif i == position_idx and \
                        potential_piece_positions[i] in opposition_army:
                        valid_move = True
                        attack = True
                    elif i == position_idx and \
                        potential_piece_positions[i] in player_army:
                        valid_move = False
                        attack = False
            #no obstructions
            if valid_move is None:
                valid_move =True
                attack = False
                
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
            if issubclass(fallen_piece, WhiteChessPiece):
                chessboard.fallen_white_army.append(fallen_piece)
            else:
                chessboard.fallen_black_army.append(fallen_piece)
            print(chessboard.fallen_black_army)
            print(chessboard.fallen_white_army)
            print(fallen_piece, fallen_piece.killed)
            
        chessboard.chessboard.loc[startpos[0],startpos[1]] = None
        chesspiece.position = endpos
        chessboard.update_board()
        chessboard.turns +=1
        player,opponent = opponent,player

""" CREATE DICTINARIES OF POTENTIAL MOVES
EG QUEEN {DIAG/HORIZONTAL[]/ VERTICAL}
ITERATE THROUGH IN ORDER
IF OPPENENT PIECE EXISTS REMOVE FOLLOWING FROM UNHINDERED
PAWNS- CHECK FORWARD DIAGONAL ONLY IF OPPONENT
KNIGHT CAN JUMP OVER PICE
"""