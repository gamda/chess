# Daniel Garcia
# gamda_yo@csu.fullerton.edu

# Assignment 6
# Game of Chess
#   Square class - "model"

# This file contains the square class, it is also
# the implementation for the graph data structure.

from chessLocals import *

def line( graph, pos, direction, ignoreKing ):
    """ This function returns a list of position tuples
        of adjacent emtpy squares, including the first non-empty
        square. It takes three parameters: the
        graph is the dict of squares, the pos is the position
        tuple in which the line should start, and the direction
        is one of the values from 'neighbor keys' in locals.py
        to indicate the direction in which the line is desired."""

    positions = []
    done = False
    setDone = False
    content = None
    while not done:
        pos = graph[pos].neighbor(direction)
        
        if( pos == None ) or setDone:
            done = True
        else:
            content = graph[pos].content
            positions.append( pos )
            
        if not ( content == EMPTY ):
            if not ignoreKing:
                setDone = True
            else:
                # see if square is occupied by king.
                # if it is a king, keep going until the
                # end of the line or another piece is found
                #   otherwise, stop like any other piece
                if( not pos == None and not( graph[pos].content == KING ) ):
                    setDone = True
                else:
                    pass# king found, do nothing

    return positions

class square:
    """ One square in a chess board. This object knows
        its neighbors, its position, if it is attacked
        by pieces on either side, and its contents:
        WHITE, BLACK, EMPTY as defined in locals.py."""

    def __init__( self , newPos ):
        self.pos = newPos# tuple
        self.whiteAttackingMe = []# list of tuples w/pos of piece attacking
        self.blackAttackingMe = []
        self.content = EMPTY
        self.contentColor = EMPTY
        self.neighbors = self._getNeighbors( newPos )# dict
        ## all objects are pickable, so no need for __getstate__
        #   or __setstate__

    def attackedByWhite( self ):
        return len(self.whiteAttackingMe) > 0

    def attackedByBlack( self ):
        return len(self.blackAttackingMe) > 0

    def neighbor( self, direction ):
        """ Returns the position tuple of the neighbor in
            the given direction. Returns None if no
            neighbor exists. 'direction' parameter should
            be picked from the neighbor keys defined in
            locals.py."""
        try:
            return self.neighbors[direction]
        except KeyError:
            return None
        # ^ try-catch added 4/19. While testing, the program crashed
        #   more than once with KeyError on TOPRIGHT, however I printed
        #   each square and its neighbors where the error occurred and
        #   all neighbor keys existed.

    def isEmpty( self ):
        return( self.content == EMPTY )

    def _getNeighbors( self , (x,y) ):
        myNeighbors = {}

        top = y+1
        btm = y-1
        left = x-1
        right = x+1
        
        if( y == 8 ):
            # top line, no top, top-left, top-right neighbor
            myNeighbors[TOP] = None
            myNeighbors[TOPLEFT] = None
            myNeighbors[TOPRIGHT] = None
            # however, we have bottom neighbor for sure
            myNeighbors[BTM] = (x,btm)
            # check right and left
            if( x == a ):
                # no left, no bottom left
                myNeighbors[LEFT] = None
                myNeighbors[BTMLEFT] = None
                # but right and btm right
                myNeighbors[RIGHT] = (right,y)
                myNeighbors[BTMRIGHT] = (right,btm)
            elif( x == h ):
                # no right, no bottom right
                myNeighbors[RIGHT] = None
                myNeighbors[BTMRIGHT] = None
                # but left and btm left
                myNeighbors[LEFT] = (left,y)
                myNeighbors[BTMLEFT] = (left,btm)
            else:
                # both right and left, with bottom
                myNeighbors[LEFT] = (left,y)
                myNeighbors[RIGHT] = (right,y)
                myNeighbors[BTMLEFT] = (left,btm)
                myNeighbors[BTMRIGHT] = (right,btm)
        elif( y == 1 ):
            # btm line, no btm, btm-left, btm-right neighbor
            myNeighbors[BTM] = None
            myNeighbors[BTMLEFT] = None
            myNeighbors[BTMRIGHT] = None
            # however, we have top neighbor for sure
            myNeighbors[TOP] = (x,top)
            # check right and left
            if( x == a ):
                # no left, no top left
                myNeighbors[LEFT] = None
                myNeighbors[TOPLEFT] = None
                # but right and top right
                myNeighbors[RIGHT] = (right,y)
                myNeighbors[TOPRIGHT] = (right,top)
            elif( x == h ):
                # no right, no top right
                myNeighbors[RIGHT] = None
                myNeighbors[BTMRIGHT] = None
                # but left and top left
                myNeighbors[LEFT] = (left,y)
                myNeighbors[TOPLEFT] = (left,top)
            else:
                # both right and left, with top
                myNeighbors[LEFT] = (left,y)
                myNeighbors[RIGHT] = (right,y)
                myNeighbors[TOPLEFT] = (left,top)
                myNeighbors[TOPRIGHT] = (right,top)
        else:
            # we have both top and bottom
            myNeighbors[TOP] = (x,y+1)
            myNeighbors[BTM] = (x,y-1)
            # check right and left
            if( x == a ):
                # no left
                myNeighbors[LEFT] = None
                myNeighbors[TOPLEFT] = None
                myNeighbors[BTMLEFT] = None
                # right w/top and btm
                myNeighbors[RIGHT] = (right,y)
                myNeighbors[TOPRIGHT] = (right,top)
                myNeighbors[BTMRIGHT] = (right,btm)
            elif( x == h ):
                # no right
                myNeighbors[RIGHT] = None
                myNeighbors[TOPRIGHT] = None
                myNeighbors[BTMRIGHT] = None
                # left w/top and btm
                myNeighbors[LEFT] = (left,y)
                myNeighbors[TOPLEFT] = (left,top)
                myNeighbors[BTMLEFT] = (left,btm)
            else:
                # all neighbors exist
                myNeighbors[LEFT] = (left,y)
                myNeighbors[TOPLEFT] = (left,top)
                myNeighbors[BTMLEFT] = (left,btm)
                myNeighbors[RIGHT] = (right,y)
                myNeighbors[TOPRIGHT] = (right,top)
                myNeighbors[BTMRIGHT] = (right,btm)
            
        return myNeighbors
            
def main():
    z = square((c,3))
    print z

if __name__ == '__main__':
    main()
