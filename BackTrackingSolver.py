
# constraints variable is list of all contraints

CONTRAINTS_DICT = dict()

def backTrackingSolver():
    return recursiveBackTracking([], constraints)

def recursiveBackTracking(assignment, constraints):
    # if assignment is complete return assignment
    if (len(validator(assignment, constraints)[0]) == 0):
        return assignment
    avaiable_wizards = wizards[:]
    for taken_wizard in assignment:
        avaiable_wizards.remove(taken_wizard)
    for wizard in avaiable_wizards:
        assignment.append(wizard)
        key = assignment[:]
        key.sort()
        if (key in CONTRAINTS_DICT):
            partial_contrains = CONTRAINTS_DICT[key];
        else:
            partial_contrains = findPartialContraints(key, contraints)
            CONTRAINTS_DICT[key] = partial_contrains
        if (len(validator(assignment, partial_contrainsconstraints)[0]) == 0):
            result = recursiveBackTracking(assignment, contraints)
            if (len(validator(result, constraints)[0]) == 0):
                return result
            assignment = assignment[:-1]
    return None


def findPartialContraints(key, contraints):
    result = set()
    for contraint in contraints:
        for variable in contraint:
            if (variable not in key):
                break
        result.add(contraint)
    return result
