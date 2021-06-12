DESCRIPTION: 
Module to emulate a multiplayer chess game in a terminal window


Module Structure
----------------

__init__.py
chess_board.py  : holds Chessboard class
chess_pieces.py : holds classes for chess pieces in game
play_chess.py   : script to play game
tests/
     __init__.py
     test_pieces.py : tests to verify movements of each piece
     test_board.py  : 


Requirements
-------------

Python 3.9

Dependencies : pandas       v1.2.4
	       tabulate     v0.8.9
	       pytest       v6.2.3


Playing the Game
-----------------
Open a terminal window and change into the directory where the package is saved
Execute command: python play_chess.py


Running Tests
-------------
Tests have been written using the pytest module

To run, open a terminal window and change into the directory where the package is saved
Execute command: pytest

