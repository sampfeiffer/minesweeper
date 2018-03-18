"""This module contains the Record class which represents a single high score record."""

from functools import total_ordering


@total_ordering
class Record(object):
    """
    This class represents a single high score record
    """

    def __init__(self, rows, cols, mines, high_score=None):
        """
        Args:
            rows (int): The total number of rows on the board
            cols (int): The total number of columns on the board
            mines (int): The total number of mines on the board
            high_score (int|None): The high score value. Defaults to None
        """

        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.high_score = high_score

    def as_tuple(self):
        """
        Gets the Record attributes as a tuple

        Returns:
            tuple<int, int, int, int>: The Record attributes as a tuple
        """

        return self.rows, self.cols, self.mines, self.high_score

    def __eq__(self, other):
        """
        Override the == operator. This is useful for sorting Record objects.
        The high_score is not included when determining if two Record objects are equal.

        Args:
            other (Record): Another Record object to compare to self
        Returns:
            bool: Are all the attributes of self and other the same?
        """

        return self.as_tuple()[:-1] == other.as_tuple()[:-1]

    def __lt__(self, other):
        """
        Override the < operator. This is useful for sorting Record objects.
        Sorting is done by rows, then cols, then mines, then high_score

        Args:
            other (Record): Another Record object to compare to self
        Returns:
            bool: Is self < other?
        """

        return self.as_tuple() < other.as_tuple()

    def __str__(self):
        """
        Returns:
            str: The attributes separated by commas
        """
        return '{},{},{},{}'.format(*self.as_tuple())


# TODO - move to test dir
if __name__ == '__main__':
    a = Record(2, 1, 1)
    b = Record(1, 2, 1)
    print [str(i) for i in sorted([a, b])]
