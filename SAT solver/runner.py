#!/usr/bin/env python

'''
    Runner for SAT_for_analysis.py.
'''


import SAT_for_analysis
import random
import os
from datetime import datetime

#folder = "dimacs_sudokus"
folder = "dimacs_sudokus"

def select_random_puzzles(folder, puzzle_count = 3000):

    filenames = [names.name for names in os.scandir(folder)]
    sample = random.sample(filenames, puzzle_count)
    with open('random_sample.txt', 'w') as outfile:

        for puzzle in sample:
            outfile.write(puzzle + '\n')

    return sample

def read_random_sample(filename):

    with open(filename) as file:
        sample = file.readlines()

    puzzles = [puzzle.rstrip() for puzzle in sample]

    return puzzles

if __name__ == '__main__':

    timestamp = datetime.now().strftime("%H-%M-%d-%m")
    #puzzles = select_random_puzzles(folder)
    puzzles = read_random_sample('random_sample.txt')

    for i, puzzle in enumerate(puzzles):
        print("Puzzle " + str(i))
        SAT_for_analysis.start_DPLL(timestamp, puzzle)
