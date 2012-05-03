Chess
=====
By Daniel Garcia
gamda_yo@csu.fullerton.edu

CS386 - Spring 2012

This project is an application designed to play
the game of chess.

DEPENDENCIES:
	All dependencies of this project are
either included, or part of Python's libraries.
The modules used are:
1. Board.py - a board class acting as controller
2. button.py - a button class that returns surface
	objects with the correct image for the 
	given button state: active, normal, and 
	disabled. Also holds button name string.
3. chessLocals.py - this module doesn't have any 
	functions. It contains constants used 
	throughout the different modules like
	directions and color.
4. dialog.py - short module used to have users
	input IP address when joining a network
	game.
5. eztext.py - module downloaded from
http://www.pygame.org/project-EzText-920-.html 
used by dialog.py to process input.
6. move.py - move class used to make moves on the 
	board and to be sent when playing a network
	game.
7. Pieces.py - contains a class for each different
	chess piece
8. square.py - contains the square class used by 
	the board to implement the graph data
	structure.

IMAGES
	The chess piece images were obtained from
http://ixian.com/chess/jin-piece-sets/. This images
were published under the Creative Commons Attribution
Share Alike 3.0 Unported License 
(http://creativecommons.org/licenses/by-sa/3.0/). The
images were created by Eric De Mund.
	All other images were developed as part of
this project.


USAGE:
	To start the application, a python 
interpreter is needed. The file that must be
executed is 'chess.py', all other files are
modules supporting the main file. To run the 
application from the command prompt:
1. Make sure you are in the project's directory
2. >> python chess.py
	Alertatively, you can open the file
using Python's IDLE and run it from there.