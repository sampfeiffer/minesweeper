import os
import pygame
from display_params import Display
from colors import BLACK, GRAY

class HighScore:
    '''
    This class keeps track of the high score and shows it on the screen.
    High scores are maintained individually for each row/col/mine setting.
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
        
        # Setup the high score
        self.high_score_file = self.get_high_score_file_name()
        self.create_high_score_file()
        self.high_score = self.get_high_score()
        
        # Draw the high score on the screen
        self.init_draw()
        self.print_high_score()
        
    def get_high_score_file_name(self):
        '''
        Gets the high score filename. Creates the 'local' directory in which the high score file sits if needed.
        
        Returns:
            str: The full high score filename (with the path)
        '''
        
        # Get the path in which the high score file sits
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        local_path = os.path.join(project_path, 'local')
        
        if not os.path.exists(local_path):
            print 'Creating local directory'
            os.makedirs(local_path)
        
        return os.path.join(local_path, 'high_score.txt')
        
    def create_high_score_file(self):
        '''Creates the high score file if it does not yet exist'''
        if not os.path.exists(self.high_score_file):
            print 'Creating high_score.txt'
            with open(self.high_score_file, 'w') as f:
                f.write('')
                
    def get_high_score(self):
        '''
        Gets the high score from the high score file. If there is no high score recorded, returns 999.
        
        Returns:
            int: The high score for this row/col/mine setting or 999 if there is no recorded high score
        '''
        
        with open(self.high_score_file, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            rows, cols, num_of_mines, high_score = [int(num) for num in line.split(',')]
            if rows == self.rows and cols == self.cols and num_of_mines == self.num_of_mines:
                return high_score
                
        return 999
        
    def init_draw(self):
        '''Defines the high score rect to show the high score'''
        self.rect = pygame.Rect(0, 0, 130, 20)

    def print_high_score(self):
        '''Prints the high score on the high score rect'''
        pygame.draw.rect(self.screen, GRAY, self.rect)
        self.screen.blit(self.get_high_score_text(), self.rect)
        
    def get_high_score_text(self):
        '''
        Returns:
            pygame.font.SysFont: The formatted high score value to show on the screen
        '''
        
        return Display.basic_font.render(' High Score: ' + str(self.high_score), True, BLACK, GRAY)
    
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
        
    def save_high_score(self):
        '''Saves the new high score to the high score file'''
        with open(self.high_score_file, 'r') as f:
            lines = f.readlines()
        
        # If there is a recorded high score for this row/col/mine setting, overwrite it
        found = False
        for i, line in enumerate(lines):
            rows, cols, num_of_mines, high_score = [int(num) for num in line.split(',')]
            if rows == self.rows and cols == self.cols and num_of_mines == self.num_of_mines:
                lines[i] = str(self) + '\n'
                found = True
                break
        
        # Otherwise, create a new entry in the high score file
        if not found:
            lines.append(str(self) + '\n')
        
        with open(self.high_score_file, 'w') as f:
            f.write(''.join(lines))
            
    def __str__(self):
        return ','.join([str(self.rows), str(self.cols), str(self.num_of_mines), str(self.high_score)])
