import pygame
from display_params import Display
from colors import BLACK, GRAY
from pics import Pics


class MineCounter:
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
        screen_width, screen_height = self.screen.get_size()
        self.screen.blit(Pics.bluemine, (Display.margin_side, screen_height - 52))
        self.rect = pygame.Rect(Display.margin_side + Pics.bluemine.get_width() + 4, screen_height - 50, 60, 40)

    def print_mine_counter(self):
        '''Prints the number of unflagged mines left on the counter rect'''
        pygame.draw.rect(self.screen, GRAY, self.rect)
        self.screen.blit(self.get_mine_counter_text(), self.rect)

    def get_mine_counter_text(self):
        '''
        Returns:
            pygame.font.SysFont: The formatted num_of_unflagged_mines value to show on the screen
        '''

        return Display.counter_font.render(str(self.num_of_unflagged_mines), True, BLACK, GRAY)

    def update(self, change_in_unflagged_mines):
        '''
        Updates the mine counter

        Args:
            change_in_unflagged_mines (int): 1 means that a tile was unflagged. -1 means that a tile was flagged.
        '''

        self.num_of_unflagged_mines += change_in_unflagged_mines
        self.print_mine_counter()
