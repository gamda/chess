# gamda_yo@csu.fullerton.edu

# Assignment 6
# Game of Chess
#   view - Pygame

# This file contains a dialog box to get the ip addresss
# for a network game, part of the "view"

import pygame, sys, eztext
from pygame.locals import *

bgColor = (228,170,30)

def getIP( ):
    pygame.init()
    basicFont = pygame.font.SysFont(None, 40)
    dialog = pygame.display.set_mode((640,240))
    dialog.fill(bgColor)
    txtBox = eztext.Input( maxlength=15, color=(0,0,0),
                           prompt='Enter IP: ' )
    # buttons
    # button texts
    strings = ["OK", "Cancel"]
    texts = []
    rects = []
    x = 400
    y = 200
    for i in range(len(strings)):
        texts.append(basicFont.render( strings[i], True,(0,0,0),bgColor))
        rects.append(texts[i].get_rect(topleft=(x,y)))
        x = x + 100
    # draw to the screen
    for i in range(len(strings)):
        dialog.blit(texts[i],rects[i])
    pygame.display.update()
    
    # create the pygame clock
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == 12:
                return
            #buttons
            if event.type == MOUSEBUTTONUP:
                for i in range(len(rects)):
                    if( rects[i].collidepoint( event.pos ) ):
                        # i is in [0,3]
                        if( i == 0 ):
                            # ok, return string
                            return txtBox.value
                        else:
                            # cancel, return none
                            return
        dialog.fill(bgColor)
        txtBox.update(events)
        txtBox.draw(dialog)
        # buttons
        for i in range(len(strings)):
            dialog.blit(texts[i],rects[i])
        pygame.display.update()

if __name__ == '__main__':
    print main()
