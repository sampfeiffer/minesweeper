'''This module contains the MineCounter class which counts how many mines still need to be flagged'''

import pygame
import display_params
import colors
import pics


class MineCounter(object):
    '''
    This class controls the mine counter for the minesweeper game
    '''

    def __init__(self, num_of_mines, screen):
        '''
        Args:
            num_of_mines (int): The total number of mines
            screen (pygame.display): The screen object
        '''

        self.num_of_unflagged_mines = num_of_mines
        self.screen = screen

        self.init_draw()
        self.print_mine_counter()

    def init_draw(self):
        '''Draws the mine symbol and defines the mine counter rect to show the number of unflagged mines left'''
        screen_height = self.screen.get_height()
        self.screen.blit(pics.BLUE_MINE, (display_params.MARGIN_SIDE, screen_height - 52))
        self.rect = pygame.Rect(display_params.MARGIN_SIDE + pics.BLUE_MINE.get_width() + 4, screen_height - 50, 60, 40)

    def print_mine_counter(self):
        '''Prints the number of unflagged mines left on the counter rect'''
        pygame.draw.rect(self.screen, colors.GRAY, self.rect)
        self.screen.blit(self.get_mine_counter_text(), self.rect)

    def get_mine_counter_text(self):
        '''
        Returns:
            pygame.font.SysFont: The formatted num_of_unflagged_mines value to show on the screen
        '''

        return display_params.COUNTER_FONT.render(str(self.num_of_unflagged_mines), True, colors.BLACK, colors.GRAY)

    def update(self, change_in_unflagged_mines):
        '''
        Updates the mine counter

        Args:
            change_in_unflagged_mines (int): 1 means that a tile was unflagged. -1 means that a tile was flagged.
        '''

        self.num_of_unflagged_mines += change_in_unflagged_mines
        self.print_mine_counter()
