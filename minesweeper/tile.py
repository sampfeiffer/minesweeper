"""This module contains the Tile class which represents a single tile on the Minesweeper board."""

import pygame
import logging
from tile_reveal_result import TileRevealResult
import display_params
import pics
import colors
logger = logging.getLogger(__name__)


class Tile(object):
    """
    This class represents a single tile on the minesweeper board
    """

    def __init__(self, row, col, screen, offset=display_params.MARGIN_SIDE):
        """
        Args:
            row (int): The row number of the tile
            col (int): The col number of the tile
            screen (pygame.display): The screen on which to draw the rect
            offset (int): The left most part of the board. Default is display_params.MARGIN_SIDE.
        """

        self.row = row
        self.col = col
        self.screen = screen

        self.location = self.get_tile_location(offset)

        self.is_shown = False
        self.is_flagged = False
        self.is_mine = False
        self.is_hovered = False
        self.value = 0
        self.color = None
        self.neighbors = []

    def get_tile_location(self, offset):
        """
        Args:
            offset (int): The left most part of the board
        Returns:
            pygame.Rect: The location of the tile on the board
        """

        left = display_params.RECT_SIZE * self.col + offset + 1
        top = display_params.RECT_SIZE * self.row + display_params.MARGIN_TOP + 1
        width = display_params.SPOT_SIZE
        height = display_params.SPOT_SIZE

        return pygame.Rect(left, top, width, height)

    def draw(self, color=colors.GRAY):
        """
        Draws the tile with the given color on the screen

        Args:
            color ((int, int, int)): The RGB color value. Defaults to GRAY.
        """

        pygame.draw.rect(self.screen, color, self.location)

    def blit(self, content, background_color=None):
        """
        Print the content on the tile

        Args:
            content (pygame.image or pygame.font): The content to show on top of the tile
            background_color ((int, int, int)): The RGB color value. Defaults to None.
        """

        if background_color is not None:
            self.draw(background_color)
        self.screen.blit(content, self.location)

    def set_mine(self):
        """Tag the tile as a mine. Add 1 to each neighbor's value."""
        self.is_mine = True
        for neighbor_tile in self.neighbors:
            neighbor_tile.value += 1

    def set_color(self):
        """
        Set the color of the tile number. For tiles with zero value or tiles with mines, the color makes no difference.
        This functions must be called after setting all the mines.
        """

        self.color = colors.COLORS[self.value]

    def is_ready_to_reveal(self):
        """
        If the tile is not flagged and not shown, it is ready to reveal.

        Returns:
            bool: Is the tile ready to reveal
        """

        return not self.is_shown and not self.is_flagged

    def left_click_down(self):
        """
        Response when the left mouse switches to the down position over the tile.
        This also applies to when the left mouse is down over another tile and then scrolled over this tile.
        """

        if self.is_ready_to_reveal():
            self.draw(colors.SOFTWHITE)

    def left_click_up(self, is_shortcut_click=False):
        """
        Reveal the tile if possible and/or trigger the shortcut click

        Args:
            is_shortcut_click (bool): Is the click a shortcut click?
        Returns:
            TileRevealResult: The aggregated tile reveal result from the tile itself and all tiles revealed via the
                shortcut click
        """

        if self.is_flagged:
            return TileRevealResult()
        else:
            if self.is_shown:
                if is_shortcut_click and self.is_fully_flagged():
                    return TileRevealResult(additional_tiles_to_reveal=self.neighbors)
                else:
                    return TileRevealResult()
            else:
                if is_shortcut_click:
                    return TileRevealResult()
                if self.is_mine:
                    return TileRevealResult(hit_mine=True, mine_tiles=[self])
                else:
                    self.show_value()
                    if self.value > 0:
                        return TileRevealResult(non_mines_uncovered=1)
                    else:
                        return TileRevealResult(non_mines_uncovered=1, additional_tiles_to_reveal=self.neighbors)

    def show_value(self):
        """Player left clicked up on an unflagged non-mine. Show the value and mark as shown."""
        logger.debug('left_click_up {} show value'.format(str(self)))
        self.is_shown = True
        text = display_params.BASIC_FONT.render(' {} '.format(' ' if self.value == 0 else self.value),
                                                True,
                                                self.color,
                                                colors.SOFTWHITE)
        self.blit(text, background_color=colors.SOFTWHITE)

    def toggle_flag(self):
        """
        Toggles the flag state

        Returns:
            int: The change in the number of mines remaining
        """

        if not self.is_shown:
            self.is_flagged = not self.is_flagged
            if self.is_flagged:
                self.blit(pics.FLAG)
                return -1
            else:
                self.draw(colors.GRAY)
                return 1

        return 0

    def hover(self, is_left_mouse_down):
        """
        If the tile is not already shown, change the color appropriately.

        Args:
            is_left_mouse_down (bool): Is the left mouse down.
        """
        if not self.is_hovered:
            self.is_hovered = True
            if not self.is_shown:
                if self.is_flagged:
                    self.blit(pics.FLAG_SCROLL)
                else:
                    self.draw(colors.SOFTWHITE if is_left_mouse_down else colors.LIGHTGRAY)

    def unhover(self):
        """If the tile is not already shown, return to base state."""
        if self.is_hovered:
            self.is_hovered = False
            if not self.is_shown:
                if self.is_flagged:
                    self.blit(pics.FLAG)
                else:
                    self.draw(colors.GRAY)

    def is_fully_flagged(self):
        """
        Checks if the neighbor tiles have the same number of flagged tiles as the tile's value

        Returns:
            bool: Is the tile fully flagged
        """

        return self.value == sum(neighbor.is_flagged for neighbor in self.neighbors)

    def reveal(self, is_losing_tile):
        """
        Reveals the tile with the correct status. This is used when the game is lost.

        Args:
            is_losing_tile (bool): Is this tile the one that was incorrectly revealed and caused the game to end?
        """

        if self.is_mine:
            if self.is_flagged:
                self.blit(pics.FLAG_MINE)
            elif is_losing_tile:
                self.blit(pics.RED_MINE)
            else:
                self.blit(pics.MINE)
        elif self.is_flagged:
            self.blit(pics.FLAG_X)

    def __str__(self):
        return 'Tile(row={}, col={}, value={}, is_mine={})'.format(self.row, self.col, self.value, self.is_mine)
