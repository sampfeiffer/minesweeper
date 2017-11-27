'''Contains the parameters used for the display.'''

import pygame


MARGIN_SIDE = 20
MARGIN_TOP = 40
MARGIN_BOTTOM = 65
SPOT_SIZE = 19
RECT_SIZE = SPOT_SIZE + 1
MIN_SCREEN_WIDTH = 350

FRAME_RATE = 50

# Fonts
pygame.font.init()
BASIC_FONT = pygame.font.SysFont(None, 24)
COUNTER_FONT = pygame.font.SysFont(None, 48)
