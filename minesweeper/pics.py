import os
import pygame

class Pics():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pics')
    
    bluemine = pygame.image.load(os.path.join(path, 'MinesweeperBlueMine.jpg'))
    clock = pygame.image.load(os.path.join(path, 'MinesweeperClock.jpg'))
    smiley = pygame.image.load(os.path.join(path, 'MinesweeperSmiley.jpg'))
    uhoh = pygame.image.load(os.path.join(path, 'MinesweeperUhOh.jpg'))
    sad = pygame.image.load(os.path.join(path, 'MinesweeperSad.jpg'))
    sunglasses = pygame.image.load(os.path.join(path, 'MinesweeperSunglass.jpg'))
    flag_scroll = pygame.image.load(os.path.join(path, 'MinesweeperFlagScroll.jpg'))
    flag = pygame.image.load(os.path.join(path, 'MinesweeperFlag.jpg'))
    mine = pygame.image.load(os.path.join(path, 'Mine.jpg'))
    red_mine = pygame.image.load(os.path.join(path, 'RedMine.jpg'))
    flag_mine = pygame.image.load(os.path.join(path, 'MineWithFlag.jpg'))
    flag_x = pygame.image.load(os.path.join(path, 'MinesweeperFlagX.jpg'))

