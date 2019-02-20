import os

def read_puzzles(folder, dim=9):

    '''Reads in sudoku puzzles from specified folder and returns them as DIMACS
    files, concatenated with general sudoku rules.'''

    ruleset = read_DIMACS('sudoku-rules.txt')

    for filename in os.scandir(folder):

        level = filename.name.split('.')[0]
        puzzle_ctr = 0

        with open(filename) as file:
            puzzles = file.readlines()

        for puz in puzzles:

            puzzle = puz.split(',')[0]

            position=0

            with open('QQwing_dimacs_sudokus/' + level + '_' + str(puzzle_ctr) + '.txt', 'w') as dimacs_file:

                for rule in ruleset:
                    dimacs_file.write(rule)

                for vertical in range(1, 1+dim):
                    for horizontal in range(1, 1+dim):

                        if puzzle[position].isdigit():
                            index = str(vertical) + str(horizontal) + str(puzzle[position])
                            dimacs_file.write(index + ' 0\n')

                        position+=1

            puzzle_ctr+=1

def read_DIMACS(filename):

    '''Read in the DIMACS file, isolating those lines with rules.'''

    DIMACS = []

    with open(filename) as file:
        data = file.readlines()

    for line in data:
        if line[0].isdigit() or line[0] == '-':
            DIMACS.append(line)

    return DIMACS

if __name__ == '__main__':
    read_puzzles('QQwing_sudokus')
