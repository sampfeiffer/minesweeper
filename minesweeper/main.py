#!/usr/bin/env python

import argparse
from game import Game


def parse_args():
    '''
    Parses the command line arguments
    
    returns:
        (argparse.Namespace): An object containing all the arguments
    '''
    
    parser = argparse.ArgumentParser(description='Starts a Minesweeper game')
    
    parser.add_argument('--rows', '-r', type=int, default=16)
    parser.add_argument('--cols', '-c', type=int, default=30)
    parser.add_argument('--mines', '-m', type=int, default=99)
    
    args = parser.parse_args()
    
    # Ensure that there are enough tiles to support the number of mines
    if args.rows * args.cols < args.mines + 9:
        raise ValueError('rows*cols must be at least 9 greater than mines')
        
    return args


if __name__ == '__main__':
    # Parse the command line arguments
    args = parse_args()
    
    # Start a game of Minesweeper
    Game(args.rows, args.cols, args.mines)
