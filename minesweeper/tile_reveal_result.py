'''This module contains the TileRevealResult class which represents the result of clicking a tile.'''

from collections import deque


class TileRevealResult(object):
    '''
    This class represents the result of clicking a tile. It supports adding together objects of the class.
    This is useful for combining the results of a shortcut click.
    '''

    def __init__(self, non_mines_uncovered=0, hit_mine=False, mine_tiles=None, additional_tiles_to_reveal=None):
        '''
        Args:
            non_mines_uncovered (int): The number of mines uncovered by the click. Defaults to 0.
            hit_mine (bool): Did the click hit a mine? Defaults to False.
            mine_tiles (list<Tile>|None): A list of tiles clicked that contain a mine or None if no tiles clicked
                contained a mine. Defaults to None.
            additional_tiles_to_reveal (list<Tile>|deque<Tile>|None): A list or deque of tiles that should also be
                revealed or None if no additional tiles need to be revealed. Defaults to None.
        '''

        self.non_mines_uncovered = non_mines_uncovered
        self.hit_mine = hit_mine
        self.mine_tiles = [] if mine_tiles is None else mine_tiles
        self.additional_tiles_to_reveal = deque() if additional_tiles_to_reveal is None else \
            deque(additional_tiles_to_reveal)

    def __add__(self, other):
        '''
        Supports adding TileRevealResult objects together.

        Args:
            other (TileRevealResult|any): Another TileRevealResult object to add to self.
                This function can handle any object though, and will just return self if other
                is not a TileRevealResult object. This is needed for taking the sum of a list of
                TileRevealResult objects since sum initializes with a 0.
        '''

        if not isinstance(other, TileRevealResult):
            return self

        self.additional_tiles_to_reveal.extend(other.additional_tiles_to_reveal)
        return TileRevealResult(self.non_mines_uncovered + other.non_mines_uncovered,
                                self.hit_mine or other.hit_mine,
                                self.mine_tiles + other.mine_tiles,
                                self.additional_tiles_to_reveal)

    def __radd__(self, other):
        return self + other

    def __str__(self):
        format_str = 'TileRevealResult(non_mines_uncovered={}, hit_mine={}, mine_tiles={}, ' + \
                     'additional_tiles_to_reveal={})'
        return format_str.format(self.non_mines_uncovered, self.hit_mine, self.mine_tiles,
                                 self.additional_tiles_to_reveal)


# TODO - move this to a test file
if __name__ == '__main__':
    print sum(TileRevealResult(i, i >= 3, [i], [i]) for i in xrange(4))
