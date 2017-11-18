import sys
import pygame
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN
from board import Board
from timer import Timer
from mine_counter import MineCounter
from reset_button import ResetButton
from high_score import HighScore
from display_params import Display
from colors import NAVYBLUE
from constants import LEFT_CLICK, RIGHT_CLICK


class Game():
    '''
    This class represents a single Minesweeper game
    '''

    def __init__(self, rows, cols, num_of_mines):
        '''
        Args:
            rows (int): The total number of rows on the board
            cols (int): The total number of columns on the board
            num_of_mines (int): The total number of mines on the board
        '''

        self.rows = rows
        self.cols = cols
        self.num_of_mines = num_of_mines

        self.initialize_screen()
        self.start_new_game()

    def initialize_screen(self):
        '''
        Initializes pygame and the game screen
        '''

        pygame.init()
        pygame.display.set_caption('Minesweeper')

        self.screen_width = max(Display.rect_size * self.cols + 2 * Display.margin_side, Display.min_screen_width)
        self.screen_height = Display.rect_size * self.rows + Display.margin_top + Display.margin_bottom
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(NAVYBLUE)

        pygame.display.update()

    def start_new_game(self):
        '''
        Starts a fresh Minesweeper game
        '''

        self.initialize_game_params()
        self.timer = Timer(self.screen)
        self.mine_counter = MineCounter(self.num_of_mines, self.screen)
        self.reset_button = ResetButton(self.screen)
        self.high_score = HighScore(self.rows, self.cols, self.num_of_mines, self.screen)
        self.board = Board(self.rows, self.cols, self.num_of_mines, self.screen)
        self.play_game()

    def initialize_game_params(self):
        '''
        Initializes several parameters needed for the game
        '''

        self.is_new_game = True
        self.is_game_over = False
        self.is_game_lost = False
        self.is_left_mouse_down = False
        self.is_right_mouse_down = False
        self.num_of_hidden_non_mines_tiles = self.rows * self.cols - self.num_of_mines

    def play_game(self):
        '''
        Main game loop. Updates timer, delays by framerate, and calls event handler.
        '''
        while True:
            if self.is_new_game or self.is_game_over:
                pygame.time.wait(1000 / Display.frame_rate)
            else:
                self.timer.update()
            self.event_handler()
            pygame.display.update()

    def event_handler(self):
        '''
        Handle any pygame event such as a mouse click or scroll.
        '''
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == LEFT_CLICK:
                self.left_mouse_down_handler(event)
            elif event.type == MOUSEBUTTONUP and event.button == LEFT_CLICK:
                self.left_mouse_up_handler(event)
            elif event.type == MOUSEBUTTONDOWN and event.button == RIGHT_CLICK:
                self.right_mouse_down_handler(event)
            elif event.type == MOUSEBUTTONUP and event.button == RIGHT_CLICK:
                self.right_mouse_up_handler(event)
            elif event.type == MOUSEMOTION:
                self.mouse_motion_handler(event)
            elif event.type == MOUSEBUTTONUP and event.button in [2, 4, 5]:
                self.shortcut_click(event)

    def left_mouse_down_handler(self, event):
        '''
        Handles a left-click-down event.

        Args:
            event (pygame.event): The pygame.event object
        '''

        self.is_left_mouse_down = True
        if not self.is_game_over:
            self.update_reset_button()

            tile = self.board.get_event_tile(event.pos)
            if tile is not None:
                self.board.update_tile_hover(tile, self.is_left_mouse_down, self.is_right_mouse_down)

    def left_mouse_up_handler(self, event):
        '''
        Handles a left-click-up event.

        Args:
            event (pygame.event): The pygame.event object
        '''

        self.is_left_mouse_down = False

        if self.reset_button.contains_event(event.pos):
            self.start_new_game()
        elif self.is_right_mouse_down:
            self.shortcut_click(event)
        else:
            tile = self.board.get_event_tile(event.pos)
            if tile is not None and not self.is_game_over:
                self.update_reset_button()
                if self.is_new_game:
                    self.first_move(tile)
                tile_reveal_result = tile.left_click_up()
                self.process_tile_reveal(tile_reveal_result)
                if not self.is_game_over:
                    self.board.update_tile_hover(tile, self.is_left_mouse_down, self.is_right_mouse_down)

    def process_tile_reveal(self, tile_reveal_result):
        '''
        Processes the result of clicking tile(s)

        Args:
            tile_reveal_result (TileRevealResult): The result of the tile reveal.
                This can potentially refer to multiple tiles revealed in a cluster or shortcut click.
        '''

        self.num_of_hidden_non_mines_tiles -= tile_reveal_result.non_mines_uncovered
        if tile_reveal_result.hit_mine:
            self.lose_game(tile_reveal_result.mine_tiles)
        elif self.num_of_hidden_non_mines_tiles == 0:
            self.win_game()

    def first_move(self, first_click_tile):
        '''
        Handles the first left-click-up on a non-flagged tile

        Args:
            first_click_tile (Tile): The tile that was clicked
        '''

        self.is_new_game = False
        self.board.first_click(first_click_tile)
        self.timer.init_clock()

    def right_mouse_down_handler(self, event):
        '''
        Handles the right-click-down event

        Args:
            event (pygame.event): The pygame.event object
        '''

        self.is_right_mouse_down = True

        tile = self.board.get_event_tile(event.pos)
        if not self.is_new_game and not self.is_game_over and tile is not None:
            if not self.is_left_mouse_down:
                change_in_unflagged_mines = tile.toggle_flag()
                self.mine_counter.update(change_in_unflagged_mines)
            self.board.update_tile_hover(tile, self.is_left_mouse_down, self.is_right_mouse_down)

    def right_mouse_up_handler(self, event):
        '''
        Handles the right-click-up event

        Args:
            event (pygame.event): The pygame.event object
        '''

        self.is_right_mouse_down = False

        if self.is_left_mouse_down:
            self.shortcut_click(event)

        tile = self.board.get_event_tile(event.pos)
        if not self.is_game_over and tile is not None:
            self.board.update_tile_hover(tile, self.is_left_mouse_down, self.is_right_mouse_down)

    def mouse_motion_handler(self, event):
        '''
        Handles the mouse motion

        Args:
            event (pygame.event): The pygame.event object
        '''

        self.reset_button.mouse_motion_handler(event.pos)

        if not self.is_game_over:
            tile = self.board.get_event_tile(event.pos)
            self.board.update_tile_hover(tile, self.is_left_mouse_down, self.is_right_mouse_down)
            self.update_reset_button()

    def shortcut_click(self, event):
        '''
        Shortcut click that reveals all revealable neighbor tiles

        Args:
            event (pygame.event): The pygame.event object
        '''

        tile = self.board.get_event_tile(event.pos)

        if not self.is_new_game and not self.is_game_over and tile is not None:
            self.update_reset_button()
            if tile.is_shown and tile.is_fully_flagged():
                tile_reveal_result = tile.left_click_up_neighbors()
                self.process_tile_reveal(tile_reveal_result)

    def lose_game(self, losing_tiles):
        '''
        The player clicked a mine. The game ends.

        Args:
            losing_tiles (list<Tile>): The list of tiles containing a mine that was revealed to end the game
        '''

        self.is_game_over = True
        self.is_game_lost = True
        self.reset_button.lost_game()
        self.board.reveal_all_tiles(losing_tiles)

    def win_game(self):
        '''The player clicked all non mine tiles. The game ends.'''
        self.board.clear_hovered_tiles_list()
        self.is_game_over = True
        self.reset_button.won_game()
        self.high_score.update(self.timer.seconds)

    def update_reset_button(self):
        '''Update the status of the reset button'''
        if self.board.hovered_tiles and self.is_left_mouse_down:
            self.reset_button.draw_uhoh()
        else:
            self.reset_button.draw_smiley()
