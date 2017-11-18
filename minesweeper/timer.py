import pygame
from display_params import Display
from colors import BLACK, GRAY
from pics import Pics


class Timer:
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
        left = screen_width - Display.margin_side - self.get_timer_text().get_width() - Pics.clock.get_width() - 10
        top = screen_height - 52
        self.screen.blit(Pics.clock, (left, top))
        self.rect = pygame.Rect(screen_width - Display.margin_side - 64, screen_height - 50, 60, 40)

    def print_time(self):
        '''Prints the time on the timer rect'''
        pygame.draw.rect(self.screen, GRAY, self.rect)
        self.screen.blit(self.get_timer_text(), self.rect)

    def get_timer_text(self):
        '''
        Returns:
            pygame.font.SysFont: The formatted timer value in seconds to show on the screen
        '''

        return Display.counter_font.render(str(self.seconds).zfill(3), True, BLACK, GRAY)

    def init_clock(self):
        '''Initialize the timer. This should be called after the player reveals the first tile.'''
        self.counter_clock = pygame.time.Clock()

    def update(self):
        '''Updates the timer. Limits the frame rate of the game to Display.frame_rate per second.'''
        self.milliseconds += self.counter_clock.tick(Display.frame_rate)
        if self.milliseconds > 1000 * self.seconds and self.seconds < 999:
            self.seconds = int(self.milliseconds / 1000.0)
            self.print_time()
