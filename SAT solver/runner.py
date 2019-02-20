#!/usr/bin/env python

'''
    Runner for SAT_for_analysis.py.
'''


import SAT_for_analysis
import random
import os
from datetime import datetime

#folder = "dimacs_sudokus"
folder = "QQwing_dimacs_sudokus"

def select_all_puzzles(folder):
    return [names.name for names in os.scandir(folder)]


if __name__ == '__main__':

    timestamp = datetime.now().strftime("%H-%M-%d-%m")
    puzzles = select_all_puzzles(folder)

    for i, puzzle in enumerate(puzzles):
        print("Puzzle " + str(i))
        SAT_for_analysis.start_DPLL(timestamp, puzzle)
