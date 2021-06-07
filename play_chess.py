from chess_board import ChessBoard

if __name__ == '__main__':
    print ('Welcome to a game of chess!')
    print (('\nTo configure symbols, confirm whether the following unicode'),
    ('chess characters are correctly represented\n\n'))

    test_symbols = [u'\u265F', u'\u265E', u'\u265C', '♚', '♕', '♝', '♘']
    print (test_symbols)
    configure_symbols = input('y/n to proceed:\t')
    if configure_symbols in ['y', 'Y', 'yes', 'YES']:
        symbol = True
    else:
        symbol = False
    print ('Initialising game.... White moves first!\n')

    chessboard = ChessBoard()
    chessboard.initialise_game(piece_unicode=symbol)