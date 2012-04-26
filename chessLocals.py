# Daniel Garcia
# gamda_yo@csu.fullerton.edu

# Assignment 6
# Game of Chess
#   locals

# This file contains constants used throughout all the other files.

## Neighbor keys
TOP = 'top'
BTM = 'btm'
LEFT = 'left'
RIGHT = 'right'
TOPLEFT = 'top-left'
TOPRIGHT = 'top-right'
BTMLEFT = 'btm-left'
BTMRIGHT = 'btm-right'

DIRECTIONS = [TOP,BTM,LEFT,RIGHT,TOPLEFT,TOPRIGHT,
           BTMLEFT,BTMRIGHT]
TOP_SQUARES = [TOP,TOPLEFT,TOPRIGHT]
BTM_SQUARES = [BTM,BTMLEFT,BTMRIGHT]

STRAIGHT_DIR = [TOP,BTM,LEFT,RIGHT]
DIAGONAL_DIR = [TOPLEFT,TOPRIGHT,BTMLEFT,BTMRIGHT]

## Ordinal value of letters for position tuples
# there's nothing special about the ordinal value
# for the program, just defining the variables
# for ease of use throughout the program
a = ord('a')
b = ord('b')
c = ord('c')
d = ord('d')
e = ord('e')
f = ord('f')
g = ord('g')
h = ord('h')
letterCoords = [a,b,c,d,e,f,g,h]
numberCoords = range(1,9)

# position tuple ex. (a,1),(h,8)

# Color variables: white, black, none
WHITE = 'W'
BLACK = 'B'
EMPTY = '_'

# Piece variables
KING = 'King'
QUEEN = 'Queen'
BISHOP = 'Bishop'
KNIGHT = 'Knight'
ROOK = 'Rook'
PAWN = 'Pawn'

# Game state variables
CHECK = 'c'
CHECKMATE = 'm'
STALEMATE = 's'
NOT_DONE = 'n'

# Move types
NORMAL = 'normal'
CASTLE = 'castle'

# Buttons states
ACTIVE = 'active'
DISABLED = 'disabled'
#NORMAL = 'normal'
