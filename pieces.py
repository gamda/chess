# Daniel Garcia
# gamda_yo@csu.fullerton.edu

# Assignment 6
# Game of Chess
#   piece classes

# This file contains the classes for each different
# piece, part of "model"

from chessLocals import *
import square

""" All pieces have:
Variables:
1. color - either white or black
2. pos - position tuple
3. iAm - char from locals.py to indicate the type of
    piece that it is
Methods:
1. move( newpos ): change position attribute
2. validMoves( squares, pieces ):
    - Parameters are the dicts declared in board class
    - Return value is a list of position tuples
3. PRIVATE      isOppositeSide( square ):
    - Parameter is a square, it contains the necessary info
    - Returns true if the pieces are on opposing teams or
        square is empty.
4. squaresAttacked( squares ):
    - Parameter is the squares dict from the board class
    - Return value is a list of position tuples. It includes
        all squares that the piece "sees" including squares
        occupied by allies and squares past the enemy king.
* King provides additional info, it knows if it has moved.
* Pawn also knows if has moved; if it hasn't, valid moves
    includes the second square if available
"""

## All variables contained in these classes are pickable
#   so no need for __getstate__ or __setstate__

class pawn:
    def __init__( self, newside, newpos ):
        self.color = newside
        self.pos = newpos
        self.iAm = PAWN
        self.hasMoved = False

    def _isOppositeSide( self, square ):
        return not (self.color == square.contentColor)

    def move( self, newpos ):
        self.pos = newpos
        self.hasMoved = True

    def validMoves( self, squares ):
        # white moves up, black moves down

        moves = []
        posToCheck = self.pos
        doneChecking = False
        
        if( self.color == WHITE ):
            # check top squares
            ###################

            # top
            posToCheck = squares[self.pos].neighbor(TOP)
            if( posToCheck ): # posToCheck != None
                if( squares[posToCheck].isEmpty() ):
                    moves.append(posToCheck)
                else:
                    doneChecking = True
            # second top square if it hasn't moved
            if not self.hasMoved and not doneChecking:
                posToCheck = squares[posToCheck].neighbor(TOP)
                if( posToCheck ): # posToCheck != None
                    if( squares[posToCheck].isEmpty() ):
                        moves.append(posToCheck)
            # top left
            posToCheck = squares[self.pos].neighbor(TOPLEFT)
            if( posToCheck ): #posToCheck != None
                if ( not squares[posToCheck].isEmpty() and \
                        self._isOppositeSide(squares[posToCheck]) ):
                    moves.append(posToCheck)
            # top right
            posToCheck = squares[self.pos].neighbor(TOPRIGHT)
            if( posToCheck ): #posToCheck != None
                if ( not squares[posToCheck].isEmpty() and \
                        self._isOppositeSide(squares[posToCheck]) ):
                    moves.append(posToCheck)
        else:
            # check bottom squares
            ######################

            # btm
            posToCheck = squares[self.pos].neighbor(BTM)
            if( posToCheck ): # posToCheck != None
                if( squares[posToCheck].isEmpty() ):
                    moves.append(posToCheck)
                else:
                    doneChecking = True
            # second btm square if it hasn't moved
            if not self.hasMoved and not doneChecking:
                posToCheck = squares[posToCheck].neighbor(BTM)
                if( posToCheck ): # posToCheck != None
                    if( squares[posToCheck].isEmpty() ):
                        moves.append(posToCheck)
            # btm left
            posToCheck = squares[self.pos].neighbor(BTMLEFT)
            if( posToCheck ): #posToCheck != None
                if ( not squares[posToCheck].isEmpty() and \
                        self._isOppositeSide(squares[posToCheck]) ):
                    moves.append(posToCheck)
            # btm right
            posToCheck = squares[self.pos].neighbor(BTMRIGHT)
            if( posToCheck ): #posToCheck != None
                if ( not squares[posToCheck].isEmpty() and \
                        self._isOppositeSide(squares[posToCheck]) ):
                    moves.append(posToCheck)
        return moves

    def squaresAttacked( self, squares ):
        attackedSquares = []
        # only two options, topleft and topright for white
        #   btmleft and btmright for black
        if( self.color == WHITE ):
            posToCheck = squares[self.pos].neighbor(TOPLEFT)
            if not( posToCheck == None ):
                attackedSquares.append(posToCheck)
            posToCheck = squares[self.pos].neighbor(TOPRIGHT)
            if not( posToCheck == None ):
                attackedSquares.append(posToCheck)
        else: # self.color == BLACK
            posToCheck = squares[self.pos].neighbor(BTMLEFT)
            if not( posToCheck == None ):
                attackedSquares.append(posToCheck)
            posToCheck = squares[self.pos].neighbor(BTMRIGHT)
            if not( posToCheck == None ):
                attackedSquares.append(posToCheck)
        return attackedSquares

class rook:
    def __init__( self, newside, newpos ):
        self.color = newside
        self.pos = newpos
        self.iAm = ROOK

    def _isOppositeSide( self, square ):
        return not (self.color == square.contentColor)

    def move( self, newpos ):
        self.pos = newpos

    def validMoves( self, squares ):
        moves = []
        for i in STRAIGHT_DIR:
            newmoves = square.line( squares, self.pos, i , False )
            if( len(newmoves) > 1 ):
                if not self._isOppositeSide( squares[newmoves[-1]] ):
                    # remove last square becaues it is an allie
                    newmoves = newmoves[0:-1]
            elif( len(newmoves) == 1 ):
                if not self._isOppositeSide( squares[newmoves[0]] ):
                    # the only move is to a square containing an allie
                    newmoves = []
            moves.extend( newmoves )
        return moves

    def squaresAttacked( self, squares ):
        attackedSquares = []
        for i in STRAIGHT_DIR:
            newSqrs = square.line( squares, self.pos, i , True )
            attackedSquares.extend( newSqrs )
        return attackedSquares

class knight:
    def __init__( self, newside, newpos ):
        self.color = newside
        self.pos = newpos
        self.iAm = KNIGHT

    def _isOppositeSide( self, square ):
        return not (self.color == square.contentColor)

    def move( self, newpos ):
        self.pos = newpos

    def validMoves( self, squares ):
        moves = []
        posToCheck = []
        x = self.pos[0]
        y = self.pos[1]
        # 8 total possible moves:
        ## top top right
        posToCheck.append((x+1,y+2))
        ## top top left
        posToCheck.append((x-1,y+2))
        ## top right right
        posToCheck.append((x+2,y+1))
        ## top left left
        posToCheck.append((x-2,y+1))
        ## btm btm right
        posToCheck.append((x+1,y-2))
        ## btm btm left
        posToCheck.append((x-1,y-2))
        ## btm right right
        posToCheck.append((x+2,y-1))
        ## btm left left
        posToCheck.append((x-2,y-1))

        for x,y in posToCheck:
            # make sure its inside
            if not( x>h or y>8 or x<a or y<1 ):
                # make sure square is empty or w/enemy
                if( squares[(x,y)].isEmpty() or
                        self._isOppositeSide(squares[(x,y)]) ):
                    moves.append((x,y))
            
        return moves

    def squaresAttacked( self, squares ):
        attackedSqrs = []
        posToCheck = []
        x = self.pos[0]
        y = self.pos[1]
        # 8 total possible moves:
        ## top top right
        posToCheck.append((x+1,y+2))
        ## top top left
        posToCheck.append((x-1,y+2))
        ## top right right
        posToCheck.append((x+2,y+1))
        ## top left left
        posToCheck.append((x-2,y+1))
        ## btm btm right
        posToCheck.append((x+1,y-2))
        ## btm btm left
        posToCheck.append((x-1,y-2))
        ## btm right right
        posToCheck.append((x+2,y-1))
        ## btm left left
        posToCheck.append((x-2,y-1))

        for x,y in posToCheck:
            # make sure its inside
            if not( x>h or y>8 or x<a or y<1 ):
                attackedSqrs.append((x,y))
        return attackedSqrs

class bishop:
    def __init__( self, newside, newpos ):
        self.color = newside
        self.pos = newpos
        self.iAm = BISHOP

    def _isOppositeSide( self, square ):
        return not (self.color == square.contentColor)

    def move( self, newpos ):
        self.pos = newpos

    def validMoves( self, squares ):
        moves = []
        for i in DIAGONAL_DIR:
            newmoves = square.line( squares, self.pos, i , False )
            if( len(newmoves) > 1 ):
                if not self._isOppositeSide( squares[newmoves[-1]] ):
                    # remove last square becaues it is an allie
                    newmoves = newmoves[0:-1]
            elif( len(newmoves) == 1 ):
                if not self._isOppositeSide( squares[newmoves[0]] ):
                    newmoves = []
            moves.extend( newmoves )
        return moves

    def squaresAttacked( self, squares ):
        attackedSquares = []
        for i in DIAGONAL_DIR:
            newSqrs = square.line( squares, self.pos, i , True )
            attackedSquares.extend( newSqrs )
        return attackedSquares

class queen:
    def __init__( self, newside, newpos ):
        self.color = newside
        self.pos = newpos
        self.iAm = QUEEN

    def _isOppositeSide( self, square ):
        return not (self.color == square.contentColor)

    def move( self, newpos ):
        self.pos = newpos

    def validMoves( self, squares ):
        moves = []
        for i in DIRECTIONS:
            newmoves = square.line( squares, self.pos, i , False )
            if( len(newmoves) > 1 ):
                if not self._isOppositeSide( squares[newmoves[-1]] ):
                    # remove last square becaues it is an allie
                    newmoves = newmoves[0:-1]
            elif( len(newmoves) == 1 ):
                if not self._isOppositeSide( squares[newmoves[0]] ):
                    newmoves = []
            moves.extend( newmoves )
        return moves

    def squaresAttacked( self, squares ):
        attackedSquares = []
        for i in DIRECTIONS:
            newSqrs = square.line( squares, self.pos, i , True )
            attackedSquares.extend( newSqrs )
        return attackedSquares

class king:
    """ Additional information: king know if it has moved, useful
        to determine if it can castle. """###validMoves() is used like in
        #all other classes, but will include castle moves if possible."""
    def __init__( self, newside, newpos ):
        self.color = newside
        self.pos = newpos
        self.iAm = KING
        #####################
        self.hasMoved = False

    def _isOppositeSide( self, square ):
        return not (self.color == square.contentColor)

    def move( self, newpos ):
        self.pos = newpos
        self.hasMoved = True

    def validMoves( self, squares ):
        moves = []
        for i in DIRECTIONS:
            neighborpos = squares[self.pos].neighbor(i)
            if( neighborpos and self._isOppositeSide( squares[neighborpos] ) ):
                # neighborpos != None and neighbor content is not ally
                if( self.color == WHITE ):
                    if not squares[neighborpos].attackedByBlack():
                        moves.append( neighborpos )
                else: #self.color == BLACK
                    if not squares[neighborpos].attackedByWhite():
                        moves.append( neighborpos )
        return moves

    def squaresAttacked( self, squares ):
        attackedSqrs = []
        for i in DIRECTIONS:
            neighborpos = squares[self.pos].neighbor(i)
            if not( neighborpos == None ):
                attackedSqrs.append( neighborpos )
        return attackedSqrs
