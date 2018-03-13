import argparse
import sys
import output_validator
import random
import time
from itertools import chain
from random import shuffle

"""
======================================================================
  Complete the following function.
======================================================================
"""

#superfast way to get around 80%
#deterministic
CONTRAINTS_DICT = dict()

def solve(num_wizards, num_constraints, wizards, constraints):
    result = recursiveBackTracking([], constraints, wizards)
    print("we got here no")
    return result

def recursiveBackTracking(assignment, constraints, wizards):
    # if assignment is complete return assignment
    if (len(assignment) == len(wizards) and your validator):
        return assignment
    avaiable_wizards = wizards[:]
    for taken_wizard in assignment:
        avaiable_wizards.remove(taken_wizard)
    for wizard in avaiable_wizards:
        assignment.append(wizard)
        key = assignment[:]
        key.sort()
        key_hashable = str(key)
        if (key_hashable in CONTRAINTS_DICT):
            partial_constraints = CONTRAINTS_DICT[key_hashable];
        else:
            partial_constraints = findPartialContraints(key, constraints)
            CONTRAINTS_DICT[key_hashable] = partial_constraints
        if (len(assignment) < 3 and your validator):
            result = recursiveBackTracking(assignment, constraints, wizards)
            if (len(assignment) == len(wizards) and your validator):
                return result
            assignment = assignment[:-1]
    return [wizards[0], wizards[1], wizards[2]]

def findPartialContraints(key, constraints):
    result = list()
    for constraint in constraints:
        toAdd = True
        for variable in constraint:
            if (variable not in key):
                toAdd = False
                break
        if (toAdd):
            result.append(constraint)
    return result

def parse_constraints(constraints):
    dct = {} #maps wizard to number of occurances
    wizToConstraint = {}
    for constraint in constraints:
        for wizard in constraint:
            if (wizard in dct):
                dct[wizard] += 1
                wizToConstraint[wizard].append(constraint)
            else:
                dct[wizard] = 1
                wizToConstraint[wizard] = []
    return dct, wizToConstraint

def swapper(lst, constraints_failed, constraints_satisfied, constraints, num_wizards, num_constraints, leftValue = 0):
    #hsh = {}
    for constraint in constraints_failed:
        wiz0 = constraint[0]
        wiz1 = constraint[1]
        wiz2 = constraint[2]
        index0 = lst.index(wiz0)
        index1 = lst.index(wiz1)
        index2 = lst.index(wiz2)

        minIndex = min(index0, index1)
        maxIndex = max(index0, index1)

        #try swapping wiz2
        minRange = range(0, minIndex + 1) #0 .... min
        maxRange = range(maxIndex, len(lst)) #...max .... end
        allowable = chain(minRange, maxRange)
        for i in allowable:
            #try swapping x with index i
            temp = lst[index2]
            lst[index2] = lst[i]
            lst[i] = temp
            failed, satisfied = validator(num_wizards, num_constraints, lst, constraints)
            if (satisfied > constraints_satisfied and index0 > leftValue and index2 > leftValue):
                return swapper(lst, failed, satisfied, constraints, num_wizards, num_constraints, leftValue)
            else:
                temp = lst[index2]
                lst[index2] = lst[i]
                lst[i] = temp



        """
        #try swapping wizard 2 with wizard 0
        temp = lst[index0]
        lst[index0] = lst[index2]
        lst[index2] = temp


        #TODO: iterate over all possible swaps

        failed, satisfied = validator(num_wizards, num_constraints, lst, constraints)

        if (satisfied > constraints_satisfied and index0 > leftValue and index2 > leftValue):
            return swapper(lst, failed, satisfied, constraints, num_wizards, num_constraints, leftValue)
        else: #unswap
            temp = lst[index0]
            lst[index0] = lst[index2]
            lst[index2] = temp

            #try swapping wizard 2 with wizard 1
            temp = lst[index1]
            lst[index1] = lst[index2]
            lst[index2] = temp


            failed, satisfied = validator(num_wizards, num_constraints, lst, constraints)

            if (satisfied > constraints_satisfied and index1 > leftValue and index2 > leftValue):
                return swapper(lst, failed, satisfied, constraints, num_wizards, num_constraints, leftValue)
            else:
                #unswap
                temp = lst[index1]
                lst[index1] = lst[index2]
                lst[index2] = temp

                temp = lst[index0]
                lst[index0] = lst[index1]
                lst[index1] = temp

                failed, satisfied = validator(num_wizards, num_constraints, lst, constraints)
                if (satisfied > constraints_satisfied and index0 > leftValue and index1 > leftValue):
                    return swapper(lst, failed, satisfied, constraints, num_wizards, num_constraints, leftValue)
                else:
                    temp = lst[index0]
                    lst[index0] = lst[index1]
                    lst[index1] = temp
        """
    return lst



def validator(num_wizards, num_constraints, output_lst, constraints):
    output_ordering_set = set(output_lst)
    output_ordering_map = {k: v for v, k in enumerate(output_lst)}

    constraints_satisfied = 0
    constraints_failed = []
    for i in range(num_constraints):
        #line_num = i + 4
        constraint = constraints[i]

        c = constraint # Creating an alias for easy reference
        m = output_ordering_map # Creating an alias for easy reference

        wiz_a = m[c[0]]
        wiz_b = m[c[1]]
        wiz_mid = m[c[2]]

        if (wiz_a < wiz_mid < wiz_b) or (wiz_b < wiz_mid < wiz_a):
            constraints_failed.append(c)
        else:
            constraints_satisfied += 1

    return  constraints_failed, constraints_satisfied

"""
======================================================================
   No need to change any code below this line
======================================================================
"""

def read_input(filename):
    with open(filename) as f:
        num_wizards = int(f.readline())
        num_constraints = int(f.readline())
        constraints = []
        wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                wizards.add(w)

    wizards = list(wizards)
    return num_wizards, num_constraints, wizards, constraints

def write_output(filename, solution):
    with open(filename, "w") as f:
        for wizard in solution:
            f.write("{0} ".format(wizard))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Constraint Solver.")
    parser.add_argument("input_file", type=str, help = "___.in")
    parser.add_argument("output_file", type=str, help = "___.out")
    args = parser.parse_args()


    start = time.clock()
    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    """
    solution = left_fix_solve(num_wizards, num_constraints, wizards, constraints, args.input_file, args.output_file)
    write_output(args.output_file, solution)
    constraints_failed, constraints_satisfied = output_validator.main([args.input_file, args.output_file])
    end = time.clock()
    print("Total time = {}".format(end - start))

    """

    while(True):


        #by constrain, random insertion
        #no limit on runtime
        solution = solve(num_wizards, num_constraints, wizards, constraints)
        constraints_failed, constraints_satisfied = validator(num_wizards, num_constraints, solution, constraints)

        solution = swapper(solution, constraints_failed, constraints_satisfied, constraints, num_wizards, num_constraints, -1)

        constraints_failed, constraints_satisfied = validator(num_wizards, num_constraints, solution, constraints)

        #greedy algorithm
        #extremely slow
        """
        solution = left_fix_solve(num_wizards, num_constraints, wizards, constraints, args.input_file, args.output_file)
        constraints_failed, constraints_satisfied = validator(num_wizards, num_constraints, solution, constraints)
        """
        if (constraints_satisfied/num_constraints >= .95):
            write_output(args.output_file, solution)
            break
