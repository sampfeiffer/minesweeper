import pygame
import display_params
from colors import BLACK, GRAY


class Display:
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

        pygame.draw.rect(self.screen, GRAY, self.rect)
        self.screen.blit(self.get_high_score_text(high_score), self.rect)

    def get_high_score_text(self, high_score):
        '''
        Args:
            high_score (int): The high score value
        Returns:
            pygame.font.SysFont: The formatted high score value to show on the screen
        '''

        return display_params.Display.basic_font.render(' High Score: ' + str(high_score), True, BLACK, GRAY)
