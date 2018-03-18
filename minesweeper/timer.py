"""This module contains the Timer class which controls the timer for the Minesweeper game."""

import pygame
import display_params
import colors
import pics


class Timer(object):
    """
    This class controls the timer for the minesweeper game
    """

    def __init__(self, screen):
        """
        Args:
            screen (pygame.display): The screen object
        """

        self.screen = screen

        self.seconds = 0
        self.milliseconds = 0

        # Print the initial timer
        self.rect = self.get_rect()
        self.draw_clock_symbol()
        self.print_time()

        self.counter_clock = None

    def get_rect(self):
        """
        Get the pygame.Rect object to show the timer.

        Returns:
             pygame.Rect: A pygame.Rect object which has the location on the the screen.
        """
        screen_width, screen_height = self.screen.get_size()
        return pygame.Rect(screen_width - display_params.MARGIN_SIDE - 64, screen_height - 50, 60, 40)

    def draw_clock_symbol(self):
        """Draws the clock symbol"""
        screen_width, screen_height = self.screen.get_size()
        left = screen_width - display_params.MARGIN_SIDE - self.get_timer_text().get_width() - pics.CLOCK.get_width() \
            - 10
        top = screen_height - 52
        self.screen.blit(pics.CLOCK, (left, top))

    def print_time(self):
        """Prints the time on the timer rect"""
        pygame.draw.rect(self.screen, colors.GRAY, self.rect)
        self.screen.blit(self.get_timer_text(), self.rect)

    def get_timer_text(self):
        """
        Returns:
            pygame.font.SysFont: The formatted timer value in seconds to show on the screen
        """

        return display_params.COUNTER_FONT.render(str(self.seconds).zfill(3), True, colors.BLACK, colors.GRAY)

    def init_clock(self):
        """Initialize the timer. This should be called after the player reveals the first tile."""
        self.counter_clock = pygame.time.Clock()

    def update(self):
        """Updates the timer. Limits the frame rate of the game to display_params.FRAME_RATE per second."""
        self.milliseconds += self.counter_clock.tick(display_params.FRAME_RATE)
        if self.milliseconds > 1000 * self.seconds and self.seconds < 999:
            self.seconds = int(self.milliseconds / 1000.0)
            self.print_time()
