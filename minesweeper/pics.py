'''This module defines several images used in the Minesweeper game'''

import os
import pygame


# The path where all the pics are located
PICS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pics')

BLUE_MINE = pygame.image.load(os.path.join(PICS_PATH, 'MinesweeperBlueMine.jpg'))
CLOCK = pygame.image.load(os.path.join(PICS_PATH, 'MinesweeperClock.jpg'))
SMILEY = pygame.image.load(os.path.join(PICS_PATH, 'MinesweeperSmiley.jpg'))
UH_OH = pygame.image.load(os.path.join(PICS_PATH, 'MinesweeperUhOh.jpg'))
SAD = pygame.image.load(os.path.join(PICS_PATH, 'MinesweeperSad.jpg'))
SUNGLASSES = pygame.image.load(os.path.join(PICS_PATH, 'MinesweeperSunglass.jpg'))
FLAG_SCROLL = pygame.image.load(os.path.join(PICS_PATH, 'MinesweeperFlagScroll.jpg'))
FLAG = pygame.image.load(os.path.join(PICS_PATH, 'MinesweeperFlag.jpg'))
MINE = pygame.image.load(os.path.join(PICS_PATH, 'Mine.jpg'))
RED_MINE = pygame.image.load(os.path.join(PICS_PATH, 'RedMine.jpg'))
FLAG_MINE = pygame.image.load(os.path.join(PICS_PATH, 'MineWithFlag.jpg'))
FLAG_X = pygame.image.load(os.path.join(PICS_PATH, 'MinesweeperFlagX.jpg'))
