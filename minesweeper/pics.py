import os
import pygame

class Pics():
    path = os.path.dirname(os.path.abspath(__file__)) + '/pics/'
    bluemine = pygame.image.load(path + 'MinesweeperBlueMine.jpg')
    clock = pygame.image.load(path + 'MinesweeperClock.jpg')
    smiley = pygame.image.load(path + 'MinesweeperSmiley.jpg')
    uhoh = pygame.image.load(path + 'MinesweeperUhOh.jpg')
    sad = pygame.image.load(path + 'MinesweeperSad.jpg')
    sunglasses = pygame.image.load(path + 'MinesweeperSunglass.jpg')
    scroll = pygame.image.load(path + 'MinesweeperFlagScroll.jpg')
    flag = pygame.image.load(path + 'MinesweeperFlag.jpg')
    mine = pygame.image.load(path + 'Mine.jpg')
    red_mine = pygame.image.load(path + 'RedMine.jpg')
    flag_mine = pygame.image.load(path + 'MineWithFlag.jpg')
    flag_x = pygame.image.load(path + 'MinesweeperFlagX.jpg')

