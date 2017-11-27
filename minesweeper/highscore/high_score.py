'''This module contains the HighScore class represents a high score for a given row/col/mine setting'''

from file_manager import FileManager
from display import Display


class HighScore(object):
    '''
    This class keeps track of the high score and shows it on the screen.
    High scores are maintained individually for each row/col/mine setting.
    '''

    def __init__(self, rows, cols, mines, screen):
        '''
        Args:
            rows (int): The total number of rows on the board
            cols (int): The total number of columns on the board
            mines (int): The total number of mines on the board
            screen (pygame.display): The screen object
        '''

        self.rows = rows
        self.cols = cols
        self.mines = mines

        # Setup the high score
        self.file_manager = FileManager()
        self.high_score = self.get_high_score()

        # Setup the high score display
        self.display = Display(screen)
        self.print_high_score()

    def get_high_score(self):
        '''
        Gets the high score from the high score file. If there is no high score recorded, returns 999.

        Returns:
            int: The high score for this row/col/mine setting or 999 if there is no recorded high score
        '''

        return self.file_manager.get_high_score(self.rows, self.cols, self.mines)

    def update(self, score):
        '''
        Updates the high score if the score was better than the previous high score.
        Prints it to the screen and records it in the high score file.

        Args:
            score (int): The new score
        '''

        if score < self.high_score:
            print 'New high score!!'
            print 'Old high score was {}'.format(self.high_score)
            self.high_score = score
            self.print_high_score()
            self.save_high_score()

    def print_high_score(self):
        '''Prints the high score on the screen'''
        self.display.print_high_score(self.high_score)

    def save_high_score(self):
        '''Saves the new high score to the high score file'''
        self.file_manager.save_high_score(self.rows, self.cols, self.mines, self.high_score)
