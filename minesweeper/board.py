'''
This module contains the Board class which represents a 2 dimensional array of Tile objects.
'''

import random
import pygame
from tile import Tile
from tile_reveal_result import TileRevealResult
import display_params
import colors


class Board(object):
    '''
    This class represents the game board - a 2 dimensional array of Tile objects
    '''

    def __init__(self, rows, cols, num_of_mines, screen):
        '''
        Args:
            rows (int): The total number of rows on the board
            cols (int): The total number of columns on the board
            num_of_mines (int): The total number of mines on the board
            screen (pygame.display): The screen object
        '''

        self.rows = rows
        self.cols = cols
        self.num_of_mines = num_of_mines
        self.screen = screen

        self.hovered_tiles = []

        self.location = self.get_location()

        # Create all the Tile objects on the board
        self.tile_grid = self.create_tiles()
        self.flattened_board = self.get_flattened_board()
        self.set_neighbors()
        self.draw()

    def get_location(self):
        '''
        Gets the location of the board

        Returns:
            pygame.Rect: The location of the board
        '''

        screen_width, screen_height = self.screen.get_size()

        width = self.cols * display_params.RECT_SIZE
        height = screen_height - (display_params.MARGIN_TOP + display_params.MARGIN_BOTTOM)
        left = (screen_width - width) / 2.0

        return pygame.Rect(left, display_params.MARGIN_TOP, width, height)

    def create_tiles(self):
        '''
        Creates the 2 dimensional array of Tile objects

        Returns:
            list<list<Tile>>: A 2-dimensional array of Tile objects
        '''

        return [[Tile(row, col, self.screen, self.location.left)
                 for col in xrange(self.cols)]
                for row in xrange(self.rows)]

    def get_flattened_board(self):
        '''
        Return a list of all the Tiles as a 1-dimensional array. This makes it easier to loop over the Tile objects.

        Returns:
            list<Tile>: A 1-dimensional array of Tile objects.
        '''

        return [tile for row in self.tile_grid for tile in row]

    def set_neighbors(self):
        '''Set the the neighbor tiles of each tile on the board'''

        # The eight directions to check for plausible neighbors
        directions = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))

        for tile in self.flattened_board:
            for direction in directions:
                neighbor_x = tile.row + direction[0]
                neighbor_y = tile.col + direction[1]
                if 0 <= neighbor_x < self.rows and 0 <= neighbor_y < self.cols:
                    tile.neighbors.append(self.tile_grid[neighbor_x][neighbor_y])

    def draw(self):
        '''Draws the board and all its tiles on the screen'''
        for tile in self.flattened_board:
            tile.draw(colors.GRAY)

        # Draw horizontal lines
        for i in xrange(self.rows + 1):
            latitude = self.location.top + i * display_params.RECT_SIZE
            pygame.draw.line(self.screen, colors.AQUA, (self.location.left, latitude), (self.location.right, latitude))

        # Draw vertical lines
        for j in xrange(self.cols + 1):
            longitude = self.location.left + j * display_params.RECT_SIZE
            pygame.draw.line(self.screen, colors.AQUA, (longitude, self.location.top),
                             (longitude, self.location.bottom))

    def first_click(self, first_click_tile):
        '''
        After the first click, set the mines, and values for each tile.

        Args:
            first_click_tile (Tile): The first tile that is clicked by the player
        '''

        self.set_mines(first_click_tile)
        self.set_tile_colors()

    def set_mines(self, first_click_tile):
        '''
        Randomly distributes the mines on the board.
        Avoids putting mines in on the first clicked tile and all it's neighbors so that the game starts with a cluster.

        Args:
            first_click_tile (Tile): The first tile that is clicked by the player
        '''

        # Figure out which tiles are off limits for mines
        cluster_one = [first_click_tile] + first_click_tile.neighbors
        legal_mine_locations = [tile for tile in self.flattened_board if tile not in cluster_one]

        # Randomly select tiles to be mines from the remaining legal locations
        tiles_with_mines = random.sample(legal_mine_locations, self.num_of_mines)
        for tile in tiles_with_mines:
            tile.set_mine()

    def set_tile_colors(self):
        '''Sets the color of each tile on the board'''
        for tile in self.flattened_board:
            tile.set_color()

    def get_event_tile(self, event_position):
        '''
        Gets the tile where the mouse is.

        Args:
            event_position ((int, int)): A tuple containing the x,y coordinates of the event
        Returns:
            Tile: The tile in which the event occured or None if the event did not occur in a tile
        '''

        # Gets the x, y coordinate of the event
        x_pos, y_pos = event_position

        # Determine the column number the mouse is in (if any)
        distance_from_left = x_pos - (self.location.left + 1)
        if distance_from_left % display_params.RECT_SIZE == display_params.SPOT_SIZE:
            return None
        else:
            col_num = distance_from_left / display_params.RECT_SIZE

        # Determine the row number the mouse is in (if any)
        distance_from_top = y_pos - (self.location.top + 1)
        if distance_from_top % display_params.RECT_SIZE == display_params.SPOT_SIZE:
            return None
        else:
            row_num = distance_from_top / display_params.RECT_SIZE

        if 0 <= row_num < self.rows and 0 <= col_num < self.cols:
            return self.tile_grid[row_num][col_num]
        else:
            return None

    def left_click_up(self, clicked_tile, is_shortcut_click=False):
        '''
        Handle a left click up on a tile.

        Args:
            clicked_tile (Tile): The tile that was clicked
            is_shortcut_click (bool): Is the click a shortcut click?
        Returns:
            TileRevealResult: The aggregated tile reveal result from the tile itself and all tiles revealed via the
                shortcut click
        '''

        tile_reveal_result = TileRevealResult(additional_tiles_to_reveal=[clicked_tile])

        while len(tile_reveal_result.additional_tiles_to_reveal) > 0:
            tile = tile_reveal_result.additional_tiles_to_reveal.popleft()
            tile_reveal_result += tile.left_click_up(is_shortcut_click)

            # Even if the original click was a shortcut click, all reveals afterwards are not shortcut clicks
            is_shortcut_click = False

        return tile_reveal_result

    def update_tile_hover(self, tile, is_left_mouse_down, is_right_mouse_down):
        '''
        Make tiles react to hover. Remove reaction from tiles no longer hovered.

        Args:
            tile (Tile or None): The tile that is currently being hovered
            is_left_mouse_down (bool): Is the left mouse currently pressed down
            is_right_mouse_down (bool): Is the right mouse currently pressed down
        '''

        is_both_mouse_down = is_left_mouse_down and is_right_mouse_down
        self.clear_hovered_tiles_list()

        if tile is not None:
            tile.hover(is_left_mouse_down)
            self.hovered_tiles.append(tile)
            if is_both_mouse_down:
                for neighbor in tile.neighbors:
                    neighbor.hover(is_left_mouse_down)

    def clear_hovered_tiles_list(self):
        '''Remove reaction from tiles no longer hovered'''
        for tile in self.hovered_tiles:
            tile.unhover()
            self.hovered_tiles.remove(tile)
            for neighbor in tile.neighbors:
                neighbor.unhover()

    def reveal_all_tiles(self, losing_tiles):
        '''
        Reveal all the tiles with the correct status. This is used when the game is lost.

        Args:
            losing_tile (list<Tile>): The list of tiles containing a mine that was revealed to end the game
        '''

        for tile in self.flattened_board:
            tile.reveal(tile in losing_tiles)
