from random import randint
from copy import copy

array = []

def expand_array(array, maxlen):

    print("appending")
    arraycopy = copy(array)
    for rand in range(randint(0, 1000)):
        arraycopy.append(2)


    if len(arraycopy) == maxlen: #success
        print("good")
        return True

    elif len(arraycopy) < maxlen:
        print("new call")
        expand_array(arraycopy, maxlen)

    else:
        print("backtrack")
        print(len(array))
        expand_array(array, maxlen)
        return False

#expand_array(array, 500)

pure_literals = 'A'
ruleset = [['A', 'B'], ['B']]
removed_clauses = [[l for l in clause if l in pure_literals] for clause in ruleset if 
c for c in ruleset for l in pure_literals in c]
print(removed_clauses)
