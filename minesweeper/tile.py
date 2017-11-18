import pygame
from tile_reveal_result import TileRevealResult
from display_params import Display
from pics import Pics
from colors import COLORS, SOFTWHITE, LIGHTGRAY, GRAY


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
            color ((int, int, int)): The RGB color value. Defaults to GRAY.
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
        '''Tag the tile as a mine. Add 1 to each neighbor's value.'''
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

    def left_click_up(self, is_shortcut_click=False):
        '''
        Reveal the tile if possible and/or trigger the shortcut click

        Args:
            is_shortcut_click (booL): Is the click a shortcut click?
        Returns:
            TileRevealResult: The aggregated tile reveal result from the tile itself and all tiles revealed via the
                shortcut click
        '''

        if self.is_flagged:
            return TileRevealResult()
        else:
            if self.is_shown:
                if is_shortcut_click:
                    return self.left_click_up_neighbors()
                else:
                    return TileRevealResult()
            else:
                if self.is_mine:
                    return TileRevealResult(hit_mine=True, mine_tiles=[self])
                else:
                    self.show_value()
                    if self.value > 0:
                        return TileRevealResult(non_mines_uncovered=1)
                    else:
                        return self.left_click_up_neighbors(non_mines_uncovered=1)

    def left_click_up_neighbors(self, non_mines_uncovered=0):
        '''
        Left click up all the neighbor tiles of the current tile.

        Args:
            non_mines_uncovered (int): How many non-mine tiles were uncovered already from this click?
        Returns:
            TileRevealResult: The aggregated tile reveal result from the tile itself and all tiles revealed via the
                shortcut click
        '''

        return TileRevealResult(non_mines_uncovered) + sum(tile.left_click_up() for tile in self.neighbors)

    def show_value(self):
        '''Player left clicked up on an unflagged non-mine. Show the value and mark as shown.'''
        self.is_shown = True
        text = Display.basic_font.render(' {} '.format(' ' if self.value == 0 else self.value),
                                         True,
                                         self.color,
                                         SOFTWHITE)
        self.blit(text, background_color=SOFTWHITE)

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

        Args:
            is_left_mouse_down (bool): Is the left mouse down.
        '''

        if not self.is_shown:
            if self.is_flagged:
                self.blit(Pics.flag_scroll)
            else:
                self.draw(SOFTWHITE if is_left_mouse_down else LIGHTGRAY)

    def unhover(self):
        '''If the tile is not flagged and not already shown, return to base state.'''
        if not self.is_shown:
            if self.is_flagged:
                self.blit(Pics.flag)
            else:
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
        return 'Tile(row={}, col={}, value={}, is_mine={})'.format(self.row, self.col, self.value, self.is_mine)
