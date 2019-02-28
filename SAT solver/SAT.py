#!/usr/bin/env python
'''
    Davis-Putnam-LL SAT solver in plain format as specified by the assignment.
    For a version with metrics/logging, check SAT_for_analysis.py.

    Implemented by Kim de Bie
'''

import sys
import random
from collections import Counter
from itertools import chain
import csv

heuristic = sys.argv[1]

def main():

    # read puzzle from command line
    puzzle = sys.argv[2]

    # save the file as ruleset
    ruleset = read_DIMACS(puzzle)

    # remove tautologies (this only has to be done once)
    ruleset = check_tautologies(ruleset)

    # call into algorithm
    solution = DP_algorithm(ruleset, [])

    # test whether the algorithm has returned a solution
    if solution:
        print('Success!')
        with open(puzzle + '.out', 'w') as outfile:

            for literal in solution:
                outfile.write(str(literal) + ' 0\n')

    else:
        print('This problem is unsatisfiable.')
        
        with open(puzzle + '.out', 'w') as outfile:
            outfile.write("")

def DP_algorithm(ruleset, assigned_literals):

    '''The DPLL algorithm. It consists of a simplifcation stage and a stage in which
    literals are assigned according to a heuristic. If the ruleset is not satisfied,
    the algorithm recursively calls itself.'''

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

    elif heuristic == "nishio":
        new_literal = assign_new_literal_nishio(ruleset)

    elif heuristic == "MOMS":
        new_literal = assign_new_literal_MOMs(ruleset)

    else:
        new_literal = assign_new_literal_random(ruleset)

    # recursively call into the algorithm with the new literal assigned
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

    '''Check for pure literals and return them as a list, plus updated ruleset.'''

    # extracting all literals present
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

    '''Checking for unit clauses and return them as a list, plus updated ruleset.'''

    assigned_literals = []

    # select all unit clauses: those with length 1
    unit_clauses = [clause for clause in ruleset if len(clause) == 1]

    while len(unit_clauses) > 0:

        # select the first unit clause that is still available
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

    '''Checks if a clause has a tautology: a literal and its negated form both occur.'''

    for literal in clause:
        if -literal in clause:
            return True
        else:
            return False


def assign_new_literal_random(ruleset):

    '''Randomly select a new literal to be assigned.'''

    all_literals = list(chain.from_iterable(ruleset))

    return random.choice(all_literals)


def assign_new_literal_MOMs(ruleset):

    '''Select a new literal to be assigned based on the MOMs heuristic.'''

    # determine minimum clause size
    minsize = min([len(clause) for clause in ruleset])

    # selecting the clauses with minimum size
    rules_selection = [clause for clause in ruleset if len(clause) == minsize]

    literal_counts = Counter()

    for clause in rules_selection:
        for literal in clause:
            literal_counts[literal] += 1

    # select the literal with the highest occurrence count in the shortest clauses
    selected_lit = max(literal_counts, key=lambda key: literal_counts[key])

    return selected_lit


def assign_new_literal_JW(ruleset):

    '''Select a new literal to be assigned based on the Jeroslow-Wang 1-sided
    heuristic.'''

    literal_counts = Counter()

    for clause in ruleset:
        for literal in clause:

            # the added value for a literal is weighted by the length of its clause
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

            # the added value for a literal is weighted by the length of its clause
            addition = 2 ** -len(clause)

            abs_counts[abs(literal)] += addition
            literal_counts[literal] += addition

    # getting the literal with the highest summed-up value
    lit = max(abs_counts, key=lambda key: abs_counts[key])

    # now extract the polarity that has the heighest weight
    selected_lit = lit if literal_counts[lit] > literal_counts[-lit] else -lit

    return selected_lit


def assign_new_literal_nishio(ruleset):

    '''Returns the literal for which there are the fewest options left.
    This is equivalent to the positive literal that has the fewest negative
    constraints.'''

    literal_counts = Counter()

    for clause in ruleset:
        for lit in clause:

            # count only negative occurrences
            if lit < 0:
                literal_counts[lit] += 1

    selected_lit = min(literal_counts, key=lambda key: literal_counts[key])

    # return the negation of the selected literal, so the positive version!
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


if __name__ == '__main__':
    main()
