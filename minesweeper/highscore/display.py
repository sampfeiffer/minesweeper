'''This module contains the Display class which controls the high score display.'''

import pygame
import display_params
import colors


class Display(object):
    '''
    This class controls the high score display on the screen
    '''

    def __init__(self, screen):
        '''
        Args:
            screen (pygame.display): The screen object
        '''

        self.screen = screen

        self.rect = pygame.Rect(0, 0, 130, 20)

    def print_high_score(self, high_score):
        '''
        Prints the high score on the high score rect

        Args:
            high_score (int): The high score value
        '''

        pygame.draw.rect(self.screen, colors.GRAY, self.rect)
        self.screen.blit(Display.get_high_score_text(high_score), self.rect)

    @staticmethod
    def get_high_score_text(high_score):
        '''
        Args:
            high_score (int): The high score value
        Returns:
            pygame.font.SysFont: The formatted high score value to show on the screen
        '''

        return display_params.BASIC_FONT.render(' High Score: ' + str(high_score), True, colors.BLACK,
                                                colors.GRAY)
