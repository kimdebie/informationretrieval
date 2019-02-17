#!/usr/bin/env python
'''
    Davis-Putnam-LL SAT solver
'''

import sys
import random
from collections import Counter
from itertools import chain

tried_assignments = 0
heuristic = sys.argv[1]


def main():

    global tried_assignments

    # read command line input
    puzzle = sys.argv[2]

    ruleset = read_DIMACS(puzzle)

    # remove tautologies (this only has to be done once)
    ruleset = check_tautologies(ruleset)

    solution = DP_algorithm(ruleset, [])

    # test whether the algorithm has returned a solution
    if solution:
        print(tried_assignments)
        #pos_sol = [value for value in solution if value > 0]
        #pos_sol.sort()
        print('Success!')

    else:
        print(tried_assignments)
        print('This problem is unsatisfiable.')

def DP_algorithm(ruleset, assigned_literals):

    # first run the simplifcation rules
    ruleset, pure_assigned = check_pure_literals(ruleset)
    ruleset, unit_assigned = check_unit_clauses(ruleset)

    assigned_literals = assigned_literals + pure_assigned + unit_assigned

    # if we have received a -1, we have failed
    if ruleset == -1:
        return []

    # if the ruleset is empty, we have found a solution
    if len(ruleset) == 0:
        return assigned_literals

    # we have not yet found a solution, so we assign a new literal
    # by the determined method and run the algorithm with it
    if heuristic == "JW":
        new_literal = assign_new_literal_JW(ruleset)

    elif heuristic == "JWTS":
        new_literal = assign_new_literal_JWTS(ruleset)

    elif heuristic == "fewestoptions":
        new_literal = assign_new_literal_FO(ruleset)

    else:
        new_literal = assign_new_literal_random(ruleset)

    # check how often we've tried something
    global tried_assignments
    tried_assignments += 1

    solution = DP_algorithm(update_ruleset(ruleset, new_literal), assigned_literals + [new_literal])

    # if we fail to find a solution, we try again with the negated literal
    if not solution:
        solution = DP_algorithm(update_ruleset(ruleset, -new_literal), assigned_literals + [-new_literal])

    return solution


def update_ruleset(ruleset, literal):

    '''Updating the ruleset: remove clauses that contain the literal, and
    remove the negation of the literal from the clauses.'''

    updated_ruleset = []

    for clause in ruleset:

        # a clause that contains the literal can now be removed
        if literal in clause:
            continue

        # a clause that contains the negated literal is updated
        if -literal in clause:
            clause = set(lit for lit in clause if lit != -literal)

            # if we have an empty clause, we have failed
            if len(clause) == 0:
                return -1

        updated_ruleset.append(clause)

    return updated_ruleset


def check_pure_literals(ruleset):

    '''Check for pure literals and return them as a list.'''

    # getting the counts of all literals
    all_literals = set(chain.from_iterable(ruleset))

    # storing pure literals
    pure_literals = []

    # a literal is pure if its negative does not occur
    for literal in all_literals:
        if -literal not in all_literals:
            pure_literals.append(literal)

    # update the ruleset: all clauses containing pure literals are now
    # satisfied, so they can be removed
    for literal in pure_literals:
        ruleset = update_ruleset(ruleset, literal)

    return ruleset, pure_literals


def check_unit_clauses(ruleset):

    '''Checking for unit clauses.'''

    assigned_literals = []

    # select all unit clauses: those with length 1
    unit_clauses = [clause for clause in ruleset if len(clause) == 1]

    while len(unit_clauses) > 0:

        # everytime, select the first unit clause that is still available
        unit_clause1 = unit_clauses[0]

        # awkwardly select the (only) element from the set
        for unit in unit_clause1:
            unit_clause = unit

        # update the ruleset: remove the unit clauses, and their negated
        # literals from within other clauses
        ruleset = update_ruleset(ruleset, unit_clause)

        assigned_literals.append(unit_clause)

        # if instead of a ruleset we received -1, we have failed (empty clause)
        if ruleset == -1:
            return -1, []

        # if the returned ruleset is empty, we have succeeded (so return it)
        if len(ruleset) == 0:
            return ruleset, assigned_literals

        # update the unit clauses
        unit_clauses = [clause for clause in ruleset if len(clause) == 1]

    return ruleset, assigned_literals


def check_tautologies(ruleset):

    '''Check for tautologies. If any, the clause may be removed.'''

    ruleset = [clause for clause in ruleset if not has_tautology(clause)]

    return ruleset


def has_tautology(clause):

    return any(value > 1 for value in Counter([abs(int(literal)) for literal in clause]).values())


def assign_new_literal_random(ruleset):

    '''Randomly select a new literal to be assigned.'''

    literal_counts = Counter()

    for clause in ruleset:
        for literal in clause:

            literal_counts[literal] += 1

    return random.choice(list(literal_counts))


def assign_new_literal_JW(ruleset):

    '''Select a new literal to be assigned based on the Jeroslow-Wang 1-sided
    heuristic.'''

    literal_counts = Counter()

    for clause in ruleset:
        for literal in clause:

            addition = 2 ** -len(clause)

            literal_counts[literal] += addition

    # getting the literal with the highest summed-up value
    selected_lit = max(literal_counts, key=lambda key: literal_counts[key])

    return selected_lit


def assign_new_literal_JWTS(ruleset):

    '''Select a new literal to be assigned based on the Jeroslow-Wang 2-sided
    heuristic.'''

    literal_counts = Counter()
    abs_counts = Counter()

    for clause in ruleset:
        for literal in clause:

            addition = 2 ** -len(clause)

            abs_counts[abs(literal)] += addition
            literal_counts[literal] += addition

    # getting the literal with the highest summed-up value
    lit = max(abs_counts, key=lambda key: abs_counts[key])

    # now extract the polarity that occurs most often
    selected_lit = lit if literal_counts[lit] > literal_counts[-lit] else -lit

    return selected_lit


def assign_new_literal_FO(ruleset):

    '''Returns the literal for which there are the fewest options left.
    Now implemented as: the positive literal that has the fewest negative
    constraints'''

    literal_counts = Counter()

    for clause in ruleset:
        for lit in clause:
            if lit < 0:
                literal_counts[lit] += 1

    selected_lit = min(literal_counts, key=lambda key: literal_counts[key])

    return -selected_lit


def read_DIMACS(filename):

    '''Read in the DIMACS file format to list of lists.'''

    DIMACS = []

    with open(filename) as file:
        data = file.readlines()

    for line in data:

        if line[0].isdigit() or line[0] == '-':

            line = set(int(x) for x in line[:-2].split())
            DIMACS.append(line)

    return DIMACS


def print_sudoku(true_vars):
    """
    Print sudoku.
    :param true_vars: List of variables that your system assigned as true. Each var should be in the form of integers.
    :return:
    """
    if len(true_vars) != 81:
        print("Wrong number of variables.")
        return
    s = []
    row = []
    for i in range(len(true_vars)):
        row.append(str(int(true_vars[i]) % 10))
        if (i+1) % 9 == 0:
            s.append(row)
            row = []

    print("╔═" + "═" + "═╦═" + "═" + "═╦═" + "═" + "═╦═" + "═" + "═╦═" + "═" + "═╦═" + "═" + "═╦═" + "═" + "═╦═" + "═" + "═╦═" + "═" + "═╗")
    print("║ "+s[0][0]+" | "+s[0][1]+" | "+s[0][2]+" ║ "+s[0][3]+" | "+s[0][4]+" | "+s[0][5]+" ║ "+s[0][6]+" | "+s[0][7]+" | "+s[0][8]+" ║")
    print("╠─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╣")
    print("║ "+s[1][0]+" | "+s[1][1]+" | "+s[1][2]+" ║ "+s[1][3]+" | "+s[1][4]+" | "+s[1][5]+" ║ "+s[1][6]+" | "+s[1][7]+" | "+s[1][8]+" ║")
    print("╠─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╣")
    print("║ "+s[2][0]+" | "+s[2][1]+" | "+s[2][2]+" ║ "+s[2][3]+" | "+s[2][4]+" | "+s[2][5]+" ║ "+s[2][6]+" | "+s[2][7]+" | "+s[2][8]+" ║")
    print("╠═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╣")
    print("║ "+s[3][0]+" | "+s[3][1]+" | "+s[3][2]+" ║ "+s[3][3]+" | "+s[3][4]+" | "+s[3][5]+" ║ "+s[3][6]+" | "+s[3][7]+" | "+s[3][8]+" ║")
    print("╠─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╣")
    print("║ "+s[4][0]+" | "+s[4][1]+" | "+s[4][2]+" ║ "+s[4][3]+" | "+s[4][4]+" | "+s[4][5]+" ║ "+s[4][6]+" | "+s[4][7]+" | "+s[4][8]+" ║")
    print("╠─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╣")
    print("║ "+s[5][0]+" | "+s[5][1]+" | "+s[5][2]+" ║ "+s[5][3]+" | "+s[5][4]+" | "+s[5][5]+" ║ "+s[5][6]+" | "+s[5][7]+" | "+s[5][8]+" ║")
    print("╠═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╬═" + "═" + "═╣")
    print("║ "+s[6][0]+" | "+s[6][1]+" | "+s[6][2]+" ║ "+s[6][3]+" | "+s[6][4]+" | "+s[6][5]+" ║ "+s[6][6]+" | "+s[6][7]+" | "+s[6][8]+" ║")
    print("╠─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╣")
    print("║ "+s[7][0]+" | "+s[7][1]+" | "+s[7][2]+" ║ "+s[7][3]+" | "+s[7][4]+" | "+s[7][5]+" ║ "+s[7][6]+" | "+s[7][7]+" | "+s[7][8]+" ║")
    print("╠─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╬─" + "─" + "─┼─" + "─" + "─┼─" + "─" + "─╣")
    print("║ "+s[8][0]+" | "+s[8][1]+" | "+s[8][2]+" ║ "+s[8][3]+" | "+s[8][4]+" | "+s[8][5]+" ║ "+s[8][6]+" | "+s[8][7]+" | "+s[8][8]+" ║")
    print("╚═" + "═" + "═╩═" + "═" + "═╩═" + "═" + "═╩═" + "═" + "═╩═" + "═" + "═╩═" + "═" + "═╩═" + "═" + "═╩═" + "═" + "═╩═" + "═" + "═╝")

def check_sudoku(true_vars):
    """
    Check sudoku.
    :param true_vars: List of variables that your system assigned as true. Each var should be in the form of integers.
    :return:
    """
    import math as m
    s = []
    row = []
    for i in range(len(true_vars)):
        row.append(str(int(true_vars[i]) % 10))
        if (i + 1) % 9 == 0:
            s.append(row)
            row = []

    correct = True
    for i in range(len(s)):
        for j in range(len(s[0])):
            for x in range(len(s)):
                if i != x and s[i][j] == s[x][j]:
                    correct = False
                    print("Repeated value in column:", j)
            for y in range(len(s[0])):
                if j != y and s[i][j] == s[i][y]:
                    correct = False
                    print("Repeated value in row:", i)
            top_left_x = int(i-i%m.sqrt(len(s)))
            top_left_y = int(j-j%m.sqrt(len(s)))
            for x in range(top_left_x, top_left_x + int(m.sqrt(len(s)))):
                for y in range(top_left_y, top_left_y + int(m.sqrt(len(s)))):
                    if i != x and j != y and s[i][j] == s[x][y]:
                        correct = False
                        print("Repeated value in cell:", (top_left_x, top_left_y))
    return correct


if __name__ == '__main__':
    main()
