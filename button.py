# Daniel Garcia
# gamda_yo@csu.fullerton.edu

# Assignment 6
# Game of Chess
#   view - Pygame

# This file contains a naive button class

import pygame
import os

class button:
    """This class is a container. Buttons have three different
        states: normal, active, and disabled. __init__ takes
        three arguments that should be the paths to the respective
        images in that order. Only normal is mandatory. There is a
        method corresponding to each state that returns a surface
        object with the proper image."""
    def __init__( self , name , normalState , activeState = None ,
                  disabledState = None ):
        self.myname = name
        self.normalPath = normalState
        self.activePath = activeState
        self.disabledPath = disabledState

    def name( self ):
        return self.myname

    def normal( self ):
        try:
            return pygame.image.load(os.path.normpath(self.normalPath))
        except:
            return None

    def active( self ):
        try:
            return pygame.image.load(os.path.normpath(self.activePath))
        except:
            return None

    def disabled( self ):
        try:
            return pygame.image.load(os.path.normpath(self.disabledPath))
        except:
            return None

    def get_rect( self,pos ):
        surface = pygame.image.load(os.path.normpath(self.normalPath))
        return surface.get_rect( topleft = pos )
