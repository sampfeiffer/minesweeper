"""This module contains the FileManager class which manages the high score file."""

import os
import csv
from record import Record


class FileManager(object):
    """
    This class manages the high score file
    """

    def __init__(self):
        """Gets the high score filename and create the file if it does not yet exist"""

        # Get the high score filename
        self.high_score_file = FileManager.get_high_score_file_name()

        # Create the high score file if it does not already exist
        self.create_high_score_file()

    @staticmethod
    def get_high_score_file_name():
        """
        Gets the high score filename. Creates the 'local' directory in which the high score file sits if needed.

        Returns:
            str: The full high score filename (with the path)
        """

        # Get the path in which the high score file sits: ../../../local/
        project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        local_dir = os.path.join(project_path, 'local')

        FileManager.create_local_dir(local_dir)

        return os.path.join(local_dir, 'high_score.csv')

    @staticmethod
    def create_local_dir(local_dir):
        """
        Creates the 'local' directory in which the high score file sits if needed

        Args:
            local_dir (str): The directory to create if it does not yet exist
        """

        if not os.path.exists(local_dir):
            print 'Creating local directory'
            os.makedirs(local_dir)

    def create_high_score_file(self):
        """Creates the high score file if it does not yet exist"""
        if not os.path.exists(self.high_score_file):
            print 'Creating high_score.txt'
            self.write_header()

    def write_header(self):
        """Writes the header to the high score file"""
        with open(self.high_score_file, 'w') as f:
            f.write('rows,cols,mines,highscore\n')

    def parse_high_score_file(self):
        """
        Parses the high score file

        Returns:
            list<Record>: A list of Record objects. Each Record object contains a single high score record.
        """

        # Read the entire high score file
        with open(self.high_score_file, 'r') as f:
            lines = csv.reader(f)

            # Return each line (except the header) parsed into a Record object
            return [FileManager.parse_high_score_line(line) for line in list(lines)[1:]]

    @staticmethod
    def parse_high_score_line(line):
        """
        Parses a single line of the high score file. This is not intended to work for the header.

        Args:
            line (list<str>): A single line of the high score file as a list of the comma separated strings
        Returns:
            Record: A Record object
        """

        rows, cols, mines, high_score = [int(num) for num in line]
        return Record(rows, cols, mines, high_score)

    def get_high_score(self, rows, cols, mines):
        """
        Gets the high score for the given rows/cols/mines. Returns 999 if no such high score exists.

        Args:
            rows (int): The total number of rows on the board
            cols (int): The total number of columns on the board
            mines (int): The total number of mines on the board
        Returns:
            int: The high score if it exists in the record file or 999 otherwise
        """

        record_to_find = Record(rows, cols, mines)

        # Return the high score if it exists in the high score file
        for record in self.parse_high_score_file():
            if record == record_to_find:
                return record.high_score

        # Otherwise, return 999
        return 999

    def save_high_score(self, rows, cols, mines, high_score):
        """
        Saves the high score for the given rows/cols/mines to the high score file

        Args:
            rows (int): The total number of rows on the board
            cols (int): The total number of columns on the board
            mines (int): The total number of mines on the board
            high_score (int): The high score value
        """

        new_record = Record(rows, cols, mines, high_score)

        # Get the list of all records
        all_high_scores = self.parse_high_score_file()

        # If the record already exists for the given rows/cols/mines, replace the record
        found = False
        for i, record in enumerate(all_high_scores):
            if record == new_record:
                all_high_scores[i] = new_record
                found = True
                break

        # Otherwise, add a new record
        if not found:
            all_high_scores.append(new_record)

        all_high_scores.sort()

        # Write the sorted records (and header) to the high score file
        self.write_header()
        with open(self.high_score_file, 'a') as f:
            output_writer = csv.writer(f)
            for record in all_high_scores:
                output_writer.writerow(record.as_tuple())
