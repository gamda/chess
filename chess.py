# Daniel Garcia
# gamda_yo@csu.fullerton.edu

# Assignment 6
# Game of Chess
#   view - Pygame

# This file contains the main user interaction, the "view"

import pygame, sys
import pickle
from pygame.locals import *

from buttonNames import *
from button import button
from board import board
from move import move
import chessLocals
import square
import pieces

pygame.init()

# set up fonts
basicFont = pygame.font.SysFont(None, 48)
infoFont = pygame.font.SysFont(None,20)

whitesTurnTxt = basicFont.render( "White's Turn", True,(0,0,0),(200,200,200))
blacksTurnTxt = basicFont.render( "Black's Turn", True,(0,0,0),(200,200,200))
checkmateTxt = basicFont.render( "Checkmate!", True,(0,0,0),(200,200,200))
checkTxt = basicFont.render( "Check!", True,(0,0,0),(200,200,200))
stalemateTxt = basicFont.render( "Stalemate!", True,(0,0,0),(200,200,200))

# window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 570
SQR_WIDTH = 65
SQR_HEIGHT = 65
MARGIN = 25

###### INITIALIZE DISPLAY #######
windowSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,32)
pygame.display.set_caption( 'Chess!' )


###### MAIN WINDOW COMPONENTS


### Window sections, board and info area
boardRect = pygame.Rect(0,0,WINDOW_WIDTH,WINDOW_HEIGHT)
boardColor = (218,160,20)
infoRect = pygame.Rect(WINDOW_HEIGHT,0,
                       WINDOW_WIDTH-WINDOW_HEIGHT,WINDOW_HEIGHT)
infoColor = (228,170,30)# a little lighter than board


### Project info
daniel = pygame.image.load('img\\myInfo.png')
myPos = ( WINDOW_HEIGHT+15,245)


### Who's turn:
# get a rect to display to screen
turnRect = pygame.Rect(WINDOW_HEIGHT+80,10,200,60)
pieceRect = pygame.Rect(WINDOW_HEIGHT+15,10,SQR_WIDTH,SQR_HEIGHT)
# ^ to display color of who's turn it is
turnTxt = pygame.image.load('img\\turnTxt.png')
turnTxt.set_colorkey((255,255,255))


### BUTTONS
btnNames = ['btnMusicOn','btnMusicOff','btnNewGame',
            'btnSaveGame','btnUndo','btnQuit']
disabledForNetwork = ['btnNewGame','btnSaveGame','btnUndo']
path, suffix = 'img/', '.png'
active, disabled = 'Active','Disabled'
xstart, ystart = WINDOW_HEIGHT+15, 330
buttons = {}
btnRects = {}
firstPass = True # to have both music buttons on the same pos
for name in btnNames:
    buttons[name] =  button(name,path+name+suffix,
                           path+name+active+suffix,path+name+disabled+suffix)
    if not firstPass:
        # only one music square
        btnRects[name] = buttons[name].get_rect((xstart,ystart))
        # only add after the first pass, means first 2 have same pos
        ystart = ystart + 45
    firstPass = False


### Promotion
# special rect to hold the 4 possibilities for pawn promotion
#   it will be placed starting around (c,3)
promoRect = pygame.Rect(MARGIN+2*SQR_WIDTH-10,\
                              MARGIN+3*SQR_WIDTH-10,\
                              4*SQR_WIDTH+20,SQR_HEIGHT+20)
promoRow = 5
promoSqrs = [ (chessLocals.c,promoRow) , (chessLocals.d,promoRow) ,\
              (chessLocals.e,promoRow) , (chessLocals.f,promoRow) ]
promoPcs = [ chessLocals.QUEEN, chessLocals.BISHOP,\
             chessLocals.KNIGHT, chessLocals.ROOK ]
global waitingForPromotion
waitingForPromotion = False

### Drag piece support
# special rect to hold the active piece
activePieceSqr = pygame.Rect(0,0,SQR_WIDTH,SQR_HEIGHT)

################# SPRITES
### squares
lightSqrImage = pygame.image.load('img\lightSqr.png').convert()
darkSqrImage = pygame.image.load('img\darkSqr.png').convert()
highlightSqr = pygame.image.load('img\highlightSqr.png').convert()
highlightSqr.set_colorkey((255,255,255))
    # make them right size
lightSqrImage = pygame.transform.scale(lightSqrImage,(SQR_WIDTH,SQR_HEIGHT))
darkSqrImage = pygame.transform.scale(darkSqrImage,(SQR_WIDTH,SQR_HEIGHT))
highlightSqr = pygame.transform.scale(highlightSqr,(SQR_WIDTH,SQR_HEIGHT))
### white pieces
wb = pygame.image.load('img\wb.png')
wk = pygame.image.load('img\wk.png')
wn = pygame.image.load('img\wn.png')
wp = pygame.image.load('img\wp.png')
wq = pygame.image.load('img\wq.png')
wr = pygame.image.load('img\wr.png')
### black pieces
bb = pygame.image.load('img\\bb.png')
bk = pygame.image.load('img\\bk.png')
bn = pygame.image.load('img\\bn.png')
bp = pygame.image.load('img\\bp.png')
bq = pygame.image.load('img\\bq.png')
br = pygame.image.load('img\\br.png')
### game state
checkmate = pygame.image.load('img\checkMate.png')
stalemate = pygame.image.load('img\staleMate.png')
check = pygame.image.load('img\check.png')
#check.set_colorkey((255,255,255))
# check needs its own rect, it is not displayed like the other 2
checkRect = pygame.Rect(WINDOW_HEIGHT+15,80,100,35)

networkGame = False

def main( ):
    ### MUSIC
    pygame.mixer.music.load('04 5.mp3')
    #pygame.mixer.music.play(-1,.2)
    musicPlaying = False   
    ### SETUP BOARD ###
    # create square dictionary
    drawX, drawY = 25,25
    squares = {}# pygame.rect objects
    # reverse number list so we get (letter,8) on top
    #   and (letter,1) on the bottom
    chessLocals.numberCoords.reverse()
    for i in chessLocals.numberCoords:
        for j in chessLocals.letterCoords:
            newPos = (j,i)
            squares[newPos] = pygame.Rect(drawX,drawY,SQR_WIDTH,SQR_HEIGHT)
            drawX += SQR_WIDTH
        drawY += SQR_HEIGHT
        drawX = 25
    chessLocals.numberCoords.reverse()

    # see if there's a saved game
    try:
        oldGame = open('queen.pkl','rb')
    except IOError:
        oldGame = None
    prevGame = savedGame( oldGame )

    if( prevGame != None ):
        # saved game exists
        Board = prevGame
    else:
        # Initialize Board
        Board = board()
    ### FINISH BOARD SETUP ###

    #### GAME LOOP
    # state variables
    startPos = None
    endPos = None
    pieceSelected = False
    pieceDragged = False
    changedPiece = False
    while True:
        for event in pygame.event.get():
            # check for QUIT event
            if event.type == QUIT:
                exitGame( )
            # if a piece is clicked, but mouse is not up, move chip
            if event.type == MOUSEBUTTONDOWN:
                # find piece clicked
                coordClicked = posClicked( event.pos , squares )
                if( coordClicked ):# coordClicked != None
                    # square was clicked
                    if ( coordClicked in Board.allies() ):
                        ############## Unselect Piece ##############
                        if ( pieceSelected == coordClicked ):
                            changedPiece = False
                        else:
                            changedPiece = True
                        ############################################
                        # a team piece was clicked, attach it to mouse position
                        pieceSelected = coordClicked
                        pieceDragged = True
                    else:
                        # empty square or enemy was clicked
                        if not pieceDragged:
                            pieceSelected = None
                            pieceDragged = False
                        
            if event.type == MOUSEBUTTONUP:
                # a click happened
                #-----------------
                ####################### BUTTONS
                for btn,rect in btnRects.iteritems():
                    if( rect.collidepoint( event.pos ) ):
                        if( btn == 'btnMusicOff' ):
                            if musicPlaying:
                                # turn off music
                                pygame.mixer.music.stop()
                            else:
                                # turn on music
                                pygame.mixer.music.play(-1,.2)
                            musicPlaying = not musicPlaying
                        if not networkGame:
                            if( btn == 'btnNewGame' ):
                                Board.reset()
                                startPos = None
                                endPos = None
                            if( btn == 'btnSaveGame' ):
                                saveGame( Board )
                            if( btn == 'btnUndo' ):
                                # lastMove != None---^
                                Board.undo( )
                        if( btn == 'btnQuit' ):
                            exitGame()

                ####################### SQUARES
                coordClicked = posClicked( event.pos , squares )
                moved = False
                if( coordClicked ):
                    ############## Unselect Piece ##############
                    if not( changedPiece ):
                        pieceSelected = None
                    ############## Pawn promotion ##############
                    if waitingForPromotion:
                        if coordClicked in promoSqrs:
                            Board.promote( promoPcs[\
                                promoSqrs.index(coordClicked)] )
                            global waitingForPromotion
                            waitingForPromotion = False
                    ############## Select and Move ##############
                    if( pieceDragged ):
                    # a piece dragged was put down, if move is valid, make it
                        if( pieceSelected ): # pieceSelected != None
                            startPos,endPos = pieceSelected,coordClicked
                            moved = movePiece( Board, pieceSelected, \
                                           coordClicked )
                    else:# only a click, however piece already found by
                        # MOUSEBUTTONDOWN
                        if( startPos == None ):
                            startPos = pieceSelected
                        else: # start pos already, get endpos and move
                            endPos = coordClicked
                            moved = movePiece( Board, startPos, endPos )
                    if moved:
                        lastMove = move(startPos,endPos)
                        startPos = None
                        endPos = None
                        pieceDragged = False
                        pieceSelected = None
                    else:
                        #lastMove = lastMove
                        startPos = pieceSelected
                        endPos = None
                        pieceDragged = False
                        #pieceSelected = pieceSelected
        # update screen after events
        updateScreen( Board , windowSurface , squares, musicPlaying ,
                      pieceSelected , pieceDragged , pygame.mouse.get_pos() )

def saveGame( Board ):
    """Save current game state."""
    output = open('queen.pkl','wb')
    pickle.dump( Board , output )
    output.close()
        
def movePiece( Board, startPos, endPos ):
    global waitingForPromotion
    nxtMove = move(startPos,endPos)
    if Board.makeMove(nxtMove):
        waitingForPromotion = Board.canPromote()
        return True
    else:
        return False
        
def posClicked( clickpos , squares ):
    """This function takes the position where the click occured and the
        square dictionary as parameter. It's return value is the position
        tuple corresponding to the square where the click happened. If no
        square was clicked, it returns None."""
    for pos, sqr in squares.iteritems():
        if sqr.collidepoint(clickpos):
            return pos
    return None

def updateScreen( Board , windowSurface , squares , musicPlaying , \
                  pieceSelected , pieceDragged , mousepos):
    # draw background
    pygame.draw.rect(windowSurface, boardColor, boardRect )
    drawPieces( Board , windowSurface , squares , \
                pieceSelected , pieceDragged, mousepos )

    # promotion area
    if( waitingForPromotion ):
        pygame.draw.rect( windowSurface, boardColor , promoRect )
        xstart = promoRect.left+10
        ystart = promoRect.top+10
        if not Board.whitesTurn:
            promoPieces = [wq,wb,wn,wr]
        else:
            promoPieces = [bq,bb,bn,br]
        for i in promoPieces:
            activePieceSqr.topleft = (xstart,ystart)
            windowSurface.blit(i,activePieceSqr)
            xstart = xstart + SQR_WIDTH
            
    # info area
    pygame.draw.rect(windowSurface, infoColor, infoRect)
    # my info
    windowSurface.blit(daniel,myPos)

    # is game over?
    gameStatus = Board.gameState()
    
    if( gameStatus == chessLocals.CHECK ):
        windowSurface.blit( check , checkRect )
    elif( gameStatus == chessLocals.CHECKMATE ):
        pygame.draw.rect( windowSurface, boardColor , promoRect )
        windowSurface.blit( checkmate , promoRect )
    elif( gameStatus == chessLocals.STALEMATE ):
        pygame.draw.rect( windowSurface, boardColor , promoRect )
        windowSurface.blit( stalemate , promoRect )
    else: #( gameStatus == chessLocals.NOT_DONE ):
        # game not done
        pass

    # buttons
    hovered = activeSqr( mousepos )
    for name,btn in btnRects.iteritems():
        ### music case is special because both buttons
        #   share a square
        if( name == 'btnMusicOff' ):
            if musicPlaying:
                btn = buttons[name]
            else:
                btn = buttons['btnMusicOn']
        ### if not music, nothing special
        else:
            btn = buttons[name]
        ### now get proper state given the button status
        if networkGame and( name in disabledForNetwork ):
                img = btn.disabled()
        elif( name == hovered ):
            # this button has mouse over it, make it active
            img = btn.active()
        else:
            img = btn.normal()
        
        if img:
            if( btn.name() == 'btnMusicOn' ):
                windowSurface.blit(img,btnRects['btnMusicOff'])
            else:
                windowSurface.blit(img,btnRects[btn.name()])
        
    # who's turn
    windowSurface.blit( turnTxt , turnRect )
    if( Board.whitesTurn ):
        windowSurface.blit( wp , pieceRect )
    else:
        windowSurface.blit( bp , pieceRect )
       
    pygame.display.update()

def activeSqr( eventpos ):
    """Returns the name of menu sqr that is being hovered over.
        If no square is found, returns None."""
    # if hovering over buttons, make them active
    for btn,rect in btnRects.iteritems():
        if( rect.collidepoint( eventpos ) ):
            return btn
    return None

def drawPieces( Board, windowSurface, squares , \
                pieceSelected , pieceDragged, mousepos ):
    # draw squares to wipe out board
    drawSquares( windowSurface, squares )

    # now pieces
    for pos, piece in Board.pieces.copy().iteritems():
        # find the type of piece
        color = piece.color
        pieceType = piece.iAm

        if( color == chessLocals.WHITE ):
            if( pieceType == chessLocals.PAWN ):
                pic = wp
            if( pieceType == chessLocals.ROOK ):
                pic = wr
            if( pieceType == chessLocals.KNIGHT ):
                pic = wn
            if( pieceType == chessLocals.BISHOP ):
                pic = wb
            if( pieceType == chessLocals.QUEEN ):
                pic = wq
            if( pieceType == chessLocals.KING ):
                pic = wk
        else: # color == chessLocals.BLACK
            if( pieceType == chessLocals.PAWN ):
                pic = bp
            if( pieceType == chessLocals.ROOK ):
                pic = br
            if( pieceType == chessLocals.KNIGHT ):
                pic = bn
            if( pieceType == chessLocals.BISHOP ):
                pic = bb
            if( pieceType == chessLocals.QUEEN ):
                pic = bq
            if( pieceType == chessLocals.KING ):
                pic = bk
        # move piece that was clicked to mouse position
        if( pieceSelected == pos ):
            # highlight square with piece currently on
            windowSurface.blit(highlightSqr,squares[pieceSelected])
            # highlight squares with possible moves
            for validPos in Board.validPieceMoves(pos):
                windowSurface.blit(highlightSqr,squares[validPos])
                #### check for castle options
                if( piece.iAm == chessLocals.KING and not piece.hasMoved ):
                    y = piece.pos[1]# 1 if white, 8 if black
                    if( Board.canCastleRight() ):
                        windowSurface.blit(highlightSqr,\
                                           squares[(chessLocals.g,y)])
                    if( Board.canCastleLeft() ):
                        windowSurface.blit(highlightSqr,\
                                           squares[(chessLocals.c,y)])
                    
            if pieceDragged:
                activePieceSqr.center = mousepos
                windowSurface.blit(pic,activePieceSqr)
            else:
                windowSurface.blit(pic,squares[pos])
        else:
            windowSurface.blit(pic,squares[pos])

def drawSquares( windowSurface , squares ):
    # chessLocals.a = ord('a') = 97
    # chessLocals.h = ord('h') = 104
    # I want (a,1) to be dark square...(odd letter,odd number) = dark
    for (x,y),rect in squares.iteritems():
        # x is the letter, y is the number
        if( x % 2 == 1):# odd letter: a,c,e,g
            if( y % 2 == 1):# odd number: 1,3,5,7
                windowSurface.blit(darkSqrImage,squares[(x,y)])
            else: # even number: 2,4,6,8
                windowSurface.blit(lightSqrImage,squares[(x,y)])
        else: # even letter: b,d,f,h
            if( y % 2 == 1):# odd number: 1,3,5,7
                windowSurface.blit(lightSqrImage,squares[(x,y)])
            else: # even number: 2,4,6,8
                windowSurface.blit(darkSqrImage,squares[(x,y)])

def savedGame( fileToRead ):
    try:
        return pickle.load( fileToRead )
    except:
        return None
    
def exitGame( ):
    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    main()
##    for i in buttons:
##        print i.name(),i.normalPath
##        print i.normal()
        
