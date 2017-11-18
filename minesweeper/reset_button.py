import pygame
from display_params import Display
from pics import Pics


class ResetButton:
    '''
    This class controls the reset button for the minesweeper game
    '''

    def __init__(self, screen):
        '''
        Args:
            screen (pygame.display): The screen object
        '''

        self.screen = screen

        self.is_hovered = False
        self.is_game_over = False
        self.is_game_lost = False
        self.is_smiley = False
        self.is_uhoh = False

        self.init_draw()

    def init_draw(self):
        '''Defines the reset button rect and draws the smiley face in the reset button'''
        screen_width, screen_height = self.screen.get_size()
        self.rect = pygame.Rect(screen_width / 2 - Pics.smiley.get_width() / 2,
                                5,
                                Pics.smiley.get_width(),
                                Pics.smiley.get_height())
        self.draw_smiley()

    def draw(self, pic):
        '''
        Prints the picture in the reset button

        Args:
            pic (pygame.image): The picture to draw
        '''

        self.screen.blit(pic, self.rect)

    def draw_uhoh(self):
        '''Prints the uhoh picture in the reset button'''
        if not self.is_uhoh:
            self.draw(Pics.uhoh)
            self.is_smiley = False
            self.is_uhoh = True

    def draw_smiley(self):
        '''Prints the smiley picture in the reset button'''
        if not self.is_smiley and not self.is_hovered:
            self.draw(Pics.smiley)
            self.is_smiley = True
            self.is_uhoh = False

    def draw_sunglasses(self):
        '''Prints the sunglasses picture in the reset button'''
        self.draw(Pics.sunglasses)
        self.is_smiley = False
        self.is_uhoh = False

    def draw_sad(self):
        '''Prints the sad picture in the reset button'''
        self.draw(Pics.sad)
        self.is_smiley = False
        self.is_uhoh = False

    def mouse_motion_handler(self, event_position):
        '''
        Handles mouse motion

        Args:
            event_position ((int, int)): A tuple containing the x,y coordinates of the event
        '''

        if self.contains_event(event_position):
            self.hover()
        else:
            self.unhover()

    def contains_event(self, event_position):
        '''
        Checks if the mouse event is in the reset button

        Args:
            event_position ((int, int)): A tuple containing the x,y coordinates of the event
        Returns:
            bool: Is the event inside the reset button
        '''

        return self.rect.collidepoint(event_position)

    def hover(self):
        '''React to the mouse hovering over the reset button'''
        if not self.is_hovered:
            self.is_hovered = True
            self.draw_uhoh()

    def unhover(self):
        '''React to the mouse not hovering over the reset button'''
        if self.is_hovered:
            self.is_hovered = False
            if self.is_game_lost:
                self.draw_sad()
            elif self.is_game_over:
                self.draw_sunglasses()
            else:
                self.draw_smiley()

    def lost_game(self):
        '''Lost the game'''
        self.is_game_over = True
        self.is_game_lost = True
        self.draw(Pics.sad)

    def won_game(self):
        '''Won the game'''
        self.is_game_over = True
        self.draw_sunglasses()
