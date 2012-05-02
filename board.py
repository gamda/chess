# Daniel Garcia
# gamda_yo@csu.fullerton.edu

# Assignment 6
# Game of Chess
#   board class

# This file contains the board class, the "controller"

from chessLocals import *
import square
import pieces
from move import move

class board:
    """ Chess board. This object keeps all the information
        regarding an active game. It contains 64 square
        objects, and the pieces in the current game stored
        in a dictionary with position tuple keys."""
    def __init__( self ):
        
        # game variables
        self.whitesTurn = True
        self.turnCount = 0
        self.moves = []
        self.temp = None
        self.hadTempMoved = False
        # this var is to restor hasMoved attribute of pawns and king
        #   when undoing:
        self.didPieceMoveBefore = False
        self.save = False
        # data objects
        self.squares = self._generateSquares()
        self.pieces = {}
        self.kings = {}

        ## all variables pickable!

        self.reset()

    def reset( self ):
        """ Sets board to a new game."""
        self.temp = None
        self.whitesTurn = True
        self.turnCount = 0
        self.pieces.clear()
        self.pieces = self._piecesNewGame()
        # update square attack info
        self._updateSquares()
        self.kings = { WHITE: (e,1), BLACK: (e,8) }

    def validPieceMoves( self , piecepos ):
        """This function returns a list of valid moves for the piece
            contained in the given position. This function differs
            from the one contained in the piece object because it
            removes all the moves that will allow the king to be in
            check after the turn."""
        moves = self.pieces[piecepos].validMoves(self.squares)
        for j in moves[:]:
            movedBefore = True
            myMove = move(self.pieces[piecepos].pos,j)
            # move piece
            if hasattr( self.pieces[piecepos] , 'hasMoved' ):
                movedBefore = self.pieces[piecepos].hasMoved
            moveMade = self.makeMove( myMove )
            if( moveMade == True ):
                self.undo( )
                if hasattr( self.pieces[piecepos] , 'hasMoved' ):
                    if not movedBefore:
                        self.pieces[piecepos].hasMoved = False
            else:
                # player is in check after this move,
                # so move is not valid
                moves.remove(j)
        return moves

    def gameState( self ):
        """This function returns the appropriate state variable
            from locals.py. Either CHECK, CHEKCMATE, STALEMATE,
            or NOT_DONE."""
        check =  self._check()
        if check:
            if self._checkMate():
                return CHECKMATE
            # else
            return CHECK
        if self._staleMate():
            return STALEMATE
        return NOT_DONE

    def _check( self ):
        """ Returns boolean."""
        kingpos = self._chooseKing()
        if self.pieces[kingpos].color == WHITE:
            return self.squares[kingpos].attackedByBlack()
        #else
        return self.squares[kingpos].attackedByWhite()

    def _staleMate( self ):
        """Stalemate is the term in chess to describe a situation
            where the king can't move, but it is not under direct
            attack (check). When this happens, the player can't
            make any moves, however he hasn't lost the game either.
            Games reaching this state are draws. Function returns
            boolean."""
        kingpos = self._chooseKing()
        canKingMove = ( len(self.pieces[kingpos].validMoves(self.squares)) > 0 )
        check = self._check()
        if not canKingMove and not check:
            # see if other pieces can move, if they can't game is over
            allies = self.allies()
            totalMoves = 0
            for piece in allies:
                moves = self.validPieceMoves( piece )
                totalMoves = totalMoves + len(moves)
                # very rare case, most likely loop ends early
                if( totalMoves > 0):
                    return( totalMoves == 0 )
        # else
        return False

    def _checkMate( self ):
        """ Returns boolean. Tests condition on current player."""
        
        if not self._check():
            return False

        kingpos = self._chooseKing()
        color = self.pieces[kingpos].color

        # if king can move, false
        if len(self.pieces[kingpos].validMoves(self.squares)) > 0:
            return False

        # get list of pieces attacking king
        attackingPieces = []
        if (color == WHITE):
            attackingPieces = self.squares[kingpos].blackAttackingMe
        else: # color == BLACK
            attackingPieces = self.squares[kingpos].whiteAttackingMe

        # if it can't move, and 2 or more pieces are attacking,
        # there is nothing the player can do in one move to get
        # rid of the check, therefore it is checkmate
        if ( len(attackingPieces) > 1 ):
            return True

        # get list of allies
        allies = self.allies()

        # at this point king can't move. If there is only one piece
        # attacking it, we can check to see if the path can be blocked
        # or the piece removed.
        canBlock = False
        
        attackerPos = attackingPieces[0]
        attackerMoves = self.pieces[attackerPos].validMoves(self.squares)
        attackerMoves.remove(kingpos)
        # ^ remove the king's position, because allies can't move there
        attackerMoves.append( attackerPos )
        # ^ to see if allies can eat attacker
        for i in allies:# i is postion tuple, startpos
            # validPieceMoves returns ONLY moves where the active king
            # is not in check after the move. If there is one or more of
            # this moves in allies, there is no checkmate
            moves = self.validPieceMoves( i )
            if( moves ): # moves is not empty list, move is available
                return False
        # else
        return True

    def canPromote( self ):
        """This functions tries to find a pawn eligible for promotion. If
            it finds one, returns True, False otherwise."""
        color = None
        found = False
        y = 0
        if( self.whitesTurn ):
            # the move that made the pawn eligible happened already, so
            #   if its white's turn, black can promote
            color = BLACK
            y = 1
        else:
            color = WHITE
            y = 8
        # find eligible pawn
        for pos,piece in self.pieces.iteritems():
            if( piece.iAm == PAWN )and( piece.color == color )\
                and( piece.pos[1] == y ):
                found = True
                break
        return found

    def promote( self, pieceType ):
        """This function will change a pawn to the type provided in the
            parameter. It should be called only if  a pawn is eligible and
            right after the pawn becomes eligible. If no pawn is eligible,
            this will return False. Parameter is a string from chessLocals
            indicating the piece desired."""
        color = None
        newPiece = None
        y = 0
        if( self.whitesTurn ):
            # the move that made the pawn eligible happened already, so
            #   if its white's turn, black can promote
            color = BLACK
            y = 1
        else:
            color = WHITE
            y = 8
        # find eligible pawn
        for pos,piece in self.pieces.iteritems():
            if( piece.iAm == PAWN )and( piece.color == color )\
                and( piece.pos[1] == y ):
                # create the requested piece
                if( pieceType == ROOK ):
                    newPiece = pieces.rook(color,pos)
                if( pieceType == KNIGHT ):
                    newPiece = pieces.knight(color,pos)
                if( pieceType == BISHOP ):
                    newPiece = pieces.bishop(color,pos)
                if( pieceType == QUEEN ):
                    newPiece = pieces.queen(color,pos)
                break
        if( newPiece ):
            self.pieces[newPiece.pos] = newPiece
            self._updateSquares()
            return True
        else:
            # either an invalid string was provided or no pawn is eligible
            return False

    def makeMove( self, moveToTry ):
        """Before making a move, this function makes sure that the move is
            valid. Move must be in the selected piece's validMoves() method,
            player must not be in check after the move is made. Return value
            is a boolean; True if move was completed, false otherwise."""
        myMove = self._validMove( moveToTry )
        madeMove = False
        
        if( myMove == True ):
            # move piece
            self._moveAndUpdate( moveToTry )
            
            if self._check():
                # player is in check after his move, so move is not valid
                self.whitesTurn = not self.whitesTurn
                self.turnCount = self.turnCount + 1
                self._updateKingDict( moveToTry )
                self._updateSquares()
                self.moves.append( moveToTry )
                self.undo( )
                return False
            # else, move is valid
            madeMove = True
        elif( myMove == False ):
            # move is not valid, nothing to do.
            # I check this state because validMoves() has three return
            # parameters; by elimination, if this evaluates to false
            # the object we received is a move.
            pass
        else:
            # now we know that myMove is a move object and that the
            # move object received contains the start and end pos
            # for the rook that will be moved because move is castle
            
            # move king
            self._moveAndUpdate( moveToTry )
            # move rook
            self._moveAndUpdate( myMove )
            # change move type
            moveToTry.type = CASTLE

            madeMove = True

        if madeMove:
            self.whitesTurn = not self.whitesTurn
            self.turnCount = self.turnCount + 1
            if isinstance( myMove, move ):
                self.moves.append( myMove )
            self.moves.append(moveToTry)
            return True
        return False

    def _moveAndUpdate( self , moveToTry ):
        """This function always returns None. It makes the appropriate
            changes with the move object given. If a piece is removed,
            this function will store it in case it needs to be restored
            with undo()."""
        startpos = moveToTry.start
        endpos = moveToTry.end
        # try to store piece that is currently in the end position
        # to avoid losing information by overwriting the value
        # corresponding to endpos key in dict
        try:
            self.temp = self.pieces[endpos]
            if hasattr( self.temp , 'hasMoved' ):
                self.hadTempMoved = self.temp.hasMoved
        except KeyError:
            self.temp = None
        # move piece, delete from old position
        if hasattr( self.pieces[startpos] , 'hasMoved' ):
            self.didPieceMoveBefore = self.pieces[startpos].hasMoved
        self.pieces[startpos].move(endpos)
        self.pieces[endpos] = self.pieces[startpos]
        del self.pieces[startpos]
        self._updateSquares()
        self._updateKingDict( moveToTry )
        return

    def undo( self ):
        """Checks the last move in the list, and reverts it."""
        lastMove = self.moves[-1]
        goBack = lastMove.inverse()
        #self._moveAndUpdate( goBack )
        startpos = goBack.start
        endpos = goBack.end
        
        if self.temp and ( self.temp.pos == startpos ):
            # we have a temp piece that must be restored
            self.pieces[endpos] = self.pieces[startpos]
            self.pieces[endpos].move(endpos)
            self.pieces[startpos] = self.temp
            if hasattr( self.temp , 'hasMoved' ):
                self.pieces[startpos].hasMoved = self.hadTempMoved
            self.temp = None
        else:
            self.pieces[endpos] = self.pieces[startpos]
            self.pieces[endpos].move(endpos)
            del self.pieces[startpos]
        if hasattr(self.pieces[endpos] , 'hasMoved' ):
            self.pieces[endpos].hasMoved = self.didPieceMoveBefore
        
        self.moves.remove(lastMove)
        # check for castle move
        if( lastMove.type == CASTLE ):
            self.undo()
        else:
            self.whitesTurn = not self.whitesTurn
            self.turnCount = self.turnCount - 1
            self._updateSquares()
            # update king dict if necessary
            self._updateKingDict( goBack )
        return

    def canCastleRight( self ):
        """Returns True if the conditions to castle right are present,
            False otherwise."""
        kingpos = self._chooseKing()
        y = self.pieces[kingpos].pos[1]
        
        if( kingpos == ( e,y ) and not self.pieces[kingpos].hasMoved ):
            # ^ takes advantage of lazy evaluation. Not all pieces have
            #   hasMoved attribute, however it only gets called if the
            #   king is in its original position. If the king is somewhere
            #   else, or another piece is in the square, the error-prone
            #   statement won't get called
            if( self.squares[(f,y)].content == EMPTY ):
                if( self.squares[(g,y)].content == EMPTY ):
                    if( self.squares[(h,y)].content == ROOK ):
                        return True
        return False

    def canCastleLeft( self ):
        """Returns True if the conditions to castle left are present,
            False otherwise."""
        kingpos = self._chooseKing()
        y = self.pieces[kingpos].pos[1]

        if( kingpos == ( e,y ) and not self.pieces[kingpos].hasMoved ):
            # ^ takes advantage of lazy evaluation. Not all pieces have
            #   hasMoved attribute, however it only gets called if the
            #   king is in its original position. If the king is somewhere
            #   else, or another piece is in the square, the error-prone
            #   statement won't get called
            if( self.squares[(d,y)].content == EMPTY ):
                if( self.squares[(c,y)].content == EMPTY ):
                    if( self.squares[(b,y)].content == EMPTY ):
                        if( self.squares[(a,y)].content == ROOK ):
                            return True
        return False

    def _validMove( self , move ):# move is a move object
        """Makes sure a move is valid. Three possible return values:
            1. True - if the piece selected can move to end square chosen
            2. False -  if it can't move to the end square
            3. Move object - if it is a castle move and it is valid, this
                returns the move object corresponding to the rook that
                must be moved along with king."""
        if move.end in self.pieces[move.start].validMoves(self.squares):
            return True

        # else: it could be a castle move, only if startpos is king
        if( move.start in self.kings.values() ):
            return self._castle( move )

        return False

    def _castle( self, moveToTry ):
        """If castle is possible, this function returns a move object
            with the start and end position of the respective rook to
            be moved. If that is the case, the player already provided
            the king's start and end position. If no castle is possible,
            the function returns false."""
        kingpos = self._chooseKing()
        kingcolor = self.pieces[kingpos].color

        if self.pieces[kingpos].hasMoved:
            return False # if king has moved, castle is not possible

        y = self.pieces[kingpos].pos[1]
        
        # check castle right
        if self._castleRight(moveToTry,kingpos): 
            return(move((h,y),(f,y)))
        # check castle left
        if self._castleLeft(moveToTry,kingpos):
            return(move((a,y),(d,y)))

        # otherwise, no castle is possible
        return False
        # all other possible king moves would be caught by validMoves()

    def _castleRight( self, move, kingpos ):
        y = self.pieces[kingpos].pos[1]
        if self.whitesTurn:
            if( move.start == (e,y) and move.end == (g,y) ):
                postocheck = self.squares[kingpos].neighbor(RIGHT)
                if self.squares[postocheck].isEmpty() and not \
                   self.squares[postocheck].attackedByBlack(): # (f,1)
                    postocheck = self.squares[postocheck].neighbor(RIGHT)
                    if self.squares[postocheck].isEmpty() and not \
                       self.squares[postocheck].attackedByBlack(): # (g,1)
                        postocheck = self.squares[postocheck].neighbor(RIGHT)
                        if self.squares[postocheck].content == ROOK: # (h,1)
                            return True
        else: #blacks turn
            if( move.start == (e,y) and move.end == (g,y) ):
                postocheck = self.squares[kingpos].neighbor(RIGHT)
                if self.squares[postocheck].isEmpty() and not \
                   self.squares[postocheck].attackedByWhite(): # (f,8)
                    postocheck = self.squares[postocheck].neighbor(RIGHT)
                    if self.squares[postocheck].isEmpty() and not \
                       self.squares[postocheck].attackedByWhite(): # (g,8)
                        postocheck = self.squares[postocheck].neighbor(RIGHT)
                        if self.squares[postocheck].content == ROOK: # (h,8)
                            return True
        return False

    def _castleLeft( self, move, kingpos ):
        y = self.pieces[kingpos].pos[1]
        if self.whitesTurn:
            if( move.start == (e,y) and move.end == (c,y) ):
                postocheck = self.squares[kingpos].neighbor(LEFT)
                if self.squares[postocheck].isEmpty() and not \
                   self.squares[postocheck].attackedByBlack(): # (d,1)
                    postocheck = self.squares[postocheck].neighbor(LEFT)
                    if self.squares[postocheck].isEmpty() and not \
                       self.squares[postocheck].attackedByBlack(): # (c,1)
                        postocheck = self.squares[postocheck].neighbor(LEFT)#(b,1)
                        postocheck = self.squares[postocheck].neighbor(LEFT)#(a,1)
                        if self.squares[postocheck].content == ROOK: # (a,1)
                            return True
        else: # blacks turn
            if( move.start == (e,y) and move.end == (c,y) ):
                postocheck = self.squares[kingpos].neighbor(LEFT)
                if self.squares[postocheck].isEmpty() and not \
                   self.squares[postocheck].attackedByWhite(): # (d,1)
                    postocheck = self.squares[postocheck].neighbor(LEFT)
                    if self.squares[postocheck].isEmpty() and not \
                       self.squares[postocheck].attackedByWhite(): # (c,1)
                        postocheck = self.squares[postocheck].neighbor(LEFT)#(b,1)
                        postocheck = self.squares[postocheck].neighbor(LEFT)#(a,1)
                        if self.squares[postocheck].content == ROOK: # (a,1)
                            return True
        return False            

    def allies( self ):
        """This function returns a list containing only the pieces belonging
            to the current player."""
        myAllies = []
        color = None
        if self.whitesTurn:
            color = WHITE
        else:
            color = BLACK
        for k,v in self.pieces.iteritems():
            if v.color == color:
                myAllies.append(k)
        return myAllies

    def enemies( self ):
        """This function returns a list containing only the pieces in the
            opposing team of the current player."""
        myEnemies = []
        color = None
        if self.whitesTurn:
            color = WHITE
        else:
            color = BLACK
        for k,v in self.pieces.iteritems():
            if not(v.color == color):
                myEnemies.append(k)
        return myEnemies
        
    def _chooseKing( self ):
        """ Returns the position of the king of the 'active' side.
            If it's white's turn, the white king's pos, black
            otherwise."""
        if self.whitesTurn:
            return self.kings[WHITE]
        #else
        return self.kings[BLACK]

    def _updateKingDict( self , move ):
        """Function to keep the kings dictionary updated. It should be
            called AFTER any move is made, it will not update if move
            didn't involve a king. Returns None always."""
        if move.start in self.kings.values():
            self.kings[self.pieces[move.end].color] = move.end
            return

    def _updateSquares( self ):
        self.squares = self._generateSquares()
        # ^ to clear properties of previous game

        # update squares contents
        for pos, piece in self.pieces.iteritems():
            self.squares[pos].content = piece.iAm
            self.squares[pos].contentColor = piece.color

        # update attackedBy...
        for pos, piece in self.pieces.iteritems():
            posToUpdate = piece.squaresAttacked( self.squares )
            for square in posToUpdate:
                if piece.color == WHITE:
                    self.squares[square].whiteAttackingMe.append(pos)
                else:# if piece.side == BLACK:
                    self.squares[square].blackAttackingMe.append(pos)
        return

    def _piecesNewGame( self ):
        """Setus up the pieces for a new game."""
        mypieces = {}

        # black pieces
        ###############
        color = BLACK

        # pawns
        y = 7
        for x in letterCoords:
            mypieces[(x,y)] = pieces.pawn(color,(x,y))

        y = 8 # for everything else
        # rooks
        mypieces[(a,y)] = pieces.rook(color,(a,y))
        mypieces[(h,y)] = pieces.rook(color,(h,y))
        # knights
        mypieces[(b,y)] = pieces.knight(color,(b,y))
        mypieces[(g,y)] = pieces.knight(color,(g,y))
        # bishops
        mypieces[(c,y)] = pieces.bishop(color,(c,y))
        mypieces[(f,y)] = pieces.bishop(color,(f,y))
        # queen
        mypieces[(d,y)] = pieces.queen(color,(d,y))
        # king
        mypieces[(e,y)] = pieces.king(color,(e,y))

        # white pieces
        ###############
        color = WHITE

        # pawns
        y = 2
        for x in letterCoords:
            mypieces[(x,y)] = pieces.pawn(color,(x,y))

        y = 1 # for everything else
        # rooks
        mypieces[(a,y)] = pieces.rook(color,(a,y))
        mypieces[(h,y)] = pieces.rook(color,(h,y))
        # knights
        mypieces[(b,y)] = pieces.knight(color,(b,y))
        mypieces[(g,y)] = pieces.knight(color,(g,y))
        # bishops
        mypieces[(c,y)] = pieces.bishop(color,(c,y))
        mypieces[(f,y)] = pieces.bishop(color,(f,y))
        # queen
        mypieces[(d,y)] = pieces.queen(color,(d,y))
        # king
        mypieces[(e,y)] = pieces.king(color,(e,y))

        return mypieces

    def _generateSquares( self ):
        newSquares = {}
        for i in letterCoords:
            for j in numberCoords:
                newPos = (i,j)
                newSquares[newPos] = square.square(newPos)
        return newSquares

def main():
    z = board()
    m = move((e,2),(e,4))#move pawn
    z.makeMove(m)
    m = move((c,7),(c,5))# move pawn
    z.makeMove(m)
    print z.gameState()
##    for pos,sqr in z.squares.iteritems():
##        print pos,sqr.contentColor,sqr.content
##        print 'attacked by white',sqr.whiteAttackingMe
##        print 'attacked by black',sqr.blackAttackingMe
if __name__ == '__main__':
    main()
