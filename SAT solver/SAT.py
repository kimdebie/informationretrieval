#!/usr/bin/env python
'''
	Davis-Putnam-LL SAT solver
'''

import sys
import random
from collections import Counter


def main():

    # read command line input
    algorithm = sys.argv[1]
    puzzle = sys.argv[2]

    ruleset = read_DIMACS(puzzle)

    # remove tautologies (this only has to be done once)
    ruleset = check_tautologies(ruleset)

    solution = DP_algorithm(ruleset, [])

    # test whether the algorithm has returned a solution
    if solution:
        pos_sol = [value for value in solution if value>0]
        print(len(pos_sol))
        print('Success!')

    else:
        print('This problem is unsatisfiable.')

def DP_algorithm(ruleset, assigned_literals):

    # first run the simplifcation rules
    ruleset, pure_assigned = check_pure_literals(ruleset)
    ruleset, unit_assigned = check_unit_clauses(ruleset)

    assigned_literals = assigned_literals + pure_assigned + unit_assigned

    # if we have received a -1, we have failed
    if ruleset == - 1:
        return []

    # if the ruleset is empty, we have found a solution
    if len(ruleset) == 0:
        return assigned_literals

    # we have not yet found a solution, so we assign a new literal and run the algorithm with it
    new_literal = assign_new_literal(ruleset)

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
            clause = [lit for lit in clause if lit != -literal]

            # if we have an empty clause, we have failed
            if len(clause) == 0:
                return -1

        updated_ruleset.append(clause)

    return updated_ruleset


def get_literal_counts(ruleset):

    '''Count how often a literal occurs in the ruleset.'''

    literal_counts = Counter()

    for clause in ruleset:
        for literal in clause:

            literal_counts[literal] += 1

    return literal_counts


def check_pure_literals(ruleset):

    '''Check for pure literals and return them as a list.'''

    # getting the counts of all literals
    literal_counts = get_literal_counts(ruleset)

    # storing pure literals
    pure_literals = []

    # a literal is pure if its negative does not occur
    for literal in list(literal_counts):
        if -literal not in literal_counts:
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

        assigned_literals += [unit_clause]

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


def assign_new_literal(ruleset):

    '''Randomly select a new literal to be assigned.'''

    literal_counts = get_literal_counts(ruleset)

    return random.choice(list(literal_counts))


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
