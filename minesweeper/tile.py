import pygame
from display_params import Display
from pics import Pics
from colors import *

class Tile:
    '''
    This class represents a single tile on the minesweeper board
    '''
    
    def __init__(self, row, col, screen, offset=Display.margin_side):
        '''
        Args:
            row (int): The row number of the tile
            col (int): The col number of the tile
            screen (pygame.display): The screen on which to draw the rect
            offset (int): The left most part of the board. Default is Display.margin_side.
        '''
        
        self.row = row
        self.col = col
        self.screen = screen
        
        self.location = self.get_tile_location(offset)
        
        self.is_shown = False
        self.is_flagged = False
        self.is_mine = False
        self.value = 0
        self.color = None
        self.neighbors = []
                                    
    def get_tile_location(self, offset):
        '''
        Args:
            offset (int): The left most part of the board
        Returns:
            pygame.Rect: The location of the tile on the board
        '''
        
        left = Display.rect_size * self.col + offset + 1
        top = Display.rect_size * self.row + Display.margin_top + 1
        width = Display.spot_size
        height = Display.spot_size
        
        return pygame.Rect(left, top, width, height)
        
    def draw(self, color=GRAY):
        '''
        Draws the tile with the given color on the screen
        
        Args:
            color ((int, int, int)): The RGB color value
        '''
        
        pygame.draw.rect(self.screen, color, self.location)
        
    def blit(self, content, background_color=None):
        '''
        Print the content on the tile
        
        Args:
            content (pygame.image or pygame.font): The content to show on top of the tile
            background_color ((int, int, int)): The RGB color value. Defaults to None.
        '''
        
        if background_color is not None:
            self.draw(background_color)
        self.screen.blit(content, self.location)
        
        
    def set_mine(self):
        '''
        Tag the tile as a mine. Add 1 to each neighbor's value.
        '''
        
        self.is_mine = True
        for neighbor_tile in self.neighbors:
            neighbor_tile.value += 1
        
    def set_color(self):
        '''
        Sets the color of the tile number. Mines and zero values color makes no difference.
        Must be called after setting all the mines
        '''
        
        self.color = COLORS[self.value]
        
    def is_ready_to_reveal(self):
        '''
        If the tile is not flagged and not shown, it is ready to reveal.
        
        Returns:
            bool: Is the tile ready to reveal
        '''
        
        return not self.is_shown and not self.is_flagged
            
    def left_click_down(self):
        '''
        Response when the left mouse switches to the down position over the tile.
        This also applies to when the left mouse is down over another tile and then scrolled over this tile.
        '''
        
        if self.is_ready_to_reveal():
            self.draw(SOFTWHITE)
            
    def left_click_up(self):
        '''
        Response when the left mouse is released over the tile
        
        Returns:
            int: The number of non-mine tiles uncovered TODO
        '''
        
        non_mines_uncovered = 0
        hit_mine = False
        if self.is_ready_to_reveal():
            self.is_shown = True
            if self.is_mine:
               hit_mine = True
            else:
                tile_click_result = self.show_value()
                non_mines_uncovered += tile_click_result['non_mines_uncovered']
                if tile_click_result['hit_mine']:
                    hit_mine = True
                    
        return {'non_mines_uncovered': non_mines_uncovered, 'hit_mine': hit_mine}
        
    def show_value(self):
        '''
        Player left clicked up on an unflagged non-mine. Show the value.
        
        Returns:
            dict: The number of non-mine tiles uncovered TODO
        '''
        
        text = Display.basic_font.render(' {0} '.format(' ' if self.value == 0 else self.value), True, self.color, SOFTWHITE)
        self.blit(text, background_color=SOFTWHITE)
        
        non_mines_uncovered = 1
        hit_mine = False
        if self.value == 0:
            tile_click_result = self.left_click_up_neighbors()
            non_mines_uncovered += tile_click_result['non_mines_uncovered']
            if tile_click_result['hit_mine']:
                hit_mine = True
        
        return {'non_mines_uncovered': non_mines_uncovered, 'hit_mine': hit_mine}
        
    def left_click_up_neighbors(self):
        '''
        Left-click-up on all the tile's negihbors
        
        Returns:
            TODO
        '''
        
        non_mines_uncovered = 0
        hit_mine = False
        
        for tile in self.neighbors:
            tile_click_result = tile.left_click_up()
            non_mines_uncovered += tile_click_result['non_mines_uncovered']
            if tile_click_result['hit_mine']:
                hit_mine = True
                
        return {'non_mines_uncovered': non_mines_uncovered, 'hit_mine': hit_mine}        
        
    def toggle_flag(self):
        '''
        Toggles the flag state
        
        Returns:
            int: The change in the number of mines remaining
        '''
        
        if not self.is_shown:
            self.is_flagged = not self.is_flagged
            if self.is_flagged:
                self.blit(Pics.flag)
                return -1
            else:
                self.draw(GRAY)
                return 1
                
        return 0
                
        
    def hover(self, is_left_mouse_down):
        '''
        If the tile is not flagged and not already shown, change the color appropriately.
        '''
        
        if self.is_ready_to_reveal():
            color = SOFTWHITE if is_left_mouse_down else LIGHTGRAY
            self.draw(color)

    def unhover(self):
        '''
        If the tile is not flagged and not already shown, return to base state.
        '''
        
        if self.is_ready_to_reveal():
            self.draw(GRAY)
            
    def is_fully_flagged(self):
        '''
        Checks if the neighbor tiles have he same number of flagged as the tile's value
        
        Returns:
            bool: Is the tile fully flagged
        '''
        
        return self.value == sum(neighbor.is_flagged for neighbor in self.neighbors)
    
    def reveal(self, is_losing_tile):
        '''
        Reveals the tile with the correct status. This is used when the game is lost.
        
        Args:
            is_losing_tile (bool): Is this tile the one that was incorrectly revealed and caused the game to end?
        '''
        
        if self.is_mine:
            if self.is_flagged:
                self.blit(Pics.flag_mine)
            elif is_losing_tile:
                self.blit(Pics.red_mine)
            else:
                self.blit(Pics.mine)
        elif self.is_flagged:
            self.blit(Pics.flag_x)
        
    def __str__(self):
        return 'Tile(' + str(self.row) + ',' + str(self.col) + ',' + str(self.value) + ',' + str(self.is_mine) + ')'