'''Thi smodule contains the Timer class which controls the timer for the Minesweeper game.'''

import pygame
import display_params
import colors
import pics


class Timer(object):
    '''
    This class controls the timer for the minesweeper game
    '''

    def __init__(self, screen):
        '''
        Args:
            screen (pygame.display): The screen object
        '''

        self.screen = screen

        self.seconds = 0
        self.milliseconds = 0

        # Print the initial timer
        self.init_draw()
        self.print_time()

    def init_draw(self):
        '''Draws the clock symbol and defines the timer rect to show the time'''
        screen_width, screen_height = self.screen.get_size()
        left = screen_width - display_params.MARGIN_SIDE - self.get_timer_text().get_width() - pics.CLOCK.get_width() \
            - 10
        top = screen_height - 52
        self.screen.blit(pics.CLOCK, (left, top))
        self.rect = pygame.Rect(screen_width - display_params.MARGIN_SIDE - 64, screen_height - 50, 60, 40)

    def print_time(self):
        '''Prints the time on the timer rect'''
        pygame.draw.rect(self.screen, colors.GRAY, self.rect)
        self.screen.blit(self.get_timer_text(), self.rect)

    def get_timer_text(self):
        '''
        Returns:
            pygame.font.SysFont: The formatted timer value in seconds to show on the screen
        '''

        return display_params.COUNTER_FONT.render(str(self.seconds).zfill(3), True, colors.BLACK, colors.GRAY)

    def init_clock(self):
        '''Initialize the timer. This should be called after the player reveals the first tile.'''
        self.counter_clock = pygame.time.Clock()

    def update(self):
        '''Updates the timer. Limits the frame rate of the game to display_params.FRAME_RATE per second.'''
        self.milliseconds += self.counter_clock.tick(display_params.FRAME_RATE)
        if self.milliseconds > 1000 * self.seconds and self.seconds < 999:
            self.seconds = int(self.milliseconds / 1000.0)
            self.print_time()
