# Daniel Garcia
# gamda_yo@csu.fullerton.edu

# Assignment 6
# Game of Chess
#   Move class - "controller"

from chessLocals import NORMAL

class move:
    """This class only has the __init__ method and the inverse()
        method. The __init__ method takes two position tuples
        as parameters. The first one is the start position, and
        the second one is the end position."""
    def __init__( self, (xstart,ystart), (xend,yend), myType = NORMAL ):
        self.start = (xstart,ystart)
        self.end = (xend,yend)
        self.type = myType

    def inverse( self ):
        """Returns a new move object with start and end
            flipped. Data members remained unchanged."""
        return move( self.end , self.start)
