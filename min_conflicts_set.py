import random
import argparse
import output_validator
import random
import time
from random import shuffle

def initial_state(wizards, constraints):
    lst = wizards[:]
    shuffle(lst)
    shuffle(constraints)
    for constraint in constraints:
        index0 = lst.index(constraint[0])
        index1 = lst.index(constraint[1])
        index2 = lst.index(constraint[2])
        if (index0 < index2 < index1 or index1 < index2 < index0):

            swap_lst = [(index0, index2), (index2, index1), (index1, index2), (index2, index0)]
            choice = random.randint(0, 3)
            #swap two elements in swap_lst[choice]
            temp = lst[swap_lst[choice][0]]
            lst[swap_lst[choice][0]] = lst[swap_lst[choice][1]]
            lst[swap_lst[choice][1]] = temp

    return lst

def solve(wizards, constraints):
    lst = initial_state(wizards, constraints)

    last_constraints_satisfied = 0
    notSeenWizards = wizards[:]

    while(True):
        constraints_failed, constraints_satisfied = validator(len(wizards), len(constraints), lst, constraints)
        if (constraints_satisfied != last_constraints_satisfied): #tried both storing previous lst and previous failed_constraints
            notSeenWizards = wizards[:]
            last_constraints_satisfied = constraints_satisfied

        if (len(constraints_failed) == 0):
            return lst
        if (not notSeenWizards):
            index1 = random.randint(0, len(lst)-1)
            index2 = random.randint(0, len(lst)-1)
            while(index2 == index1):
                index2 = random.randint(0, len(lst)-1)

            temp = lst[index1]
            lst[index1] = lst[index2]
            lst[index2] = temp

            notSeenWizards = wizards[:]
            continue

        selected_wizard = random.choice(notSeenWizards)
        notSeenWizards.remove(selected_wizard)

        wiz_location = lst.index(selected_wizard)
        swap_index, minimum_swap = best_swap_index(wiz_location, lst, constraints, len(constraints_failed))
        insert_index, minimum_insert = best_insertion_index(selected_wizard, lst, constraints, len(constraints_failed))

        if (0.01 >= random.random()):

            index1 = lst.index(selected_wizard)
            index2 = random.randint(0, len(lst)-1)
            temp = lst[index1]
            lst[index1] = lst[index2]
            lst[index2] = temp
        elif ((minimum_swap < minimum_insert and swap_index != -1) or
            (swap_index != -1 and minimum_swap == minimum_insert and random.randint(0, 1) == 1)):
            temp = lst[swap_index]
            lst[swap_index] = lst[wiz_location]
            lst[wiz_location] = temp
        elif (minimum_insert < minimum_swap and insert_index != -1):
            lst.remove(selected_wizard)
            lst.insert(insert_index, selected_wizard)
    return []


def best_insertion_index(selected_wizard, lst, constraints, number_constraints_failed):
    lstcpy = lst[:]
    best_insertion_index = -1
    minimum = number_constraints_failed
    for i in range(len(lst)):
        lstcpy.remove(selected_wizard)
        lstcpy.insert(i, selected_wizard)
        constraints_failed, constraints_satisfied = validator(len(lst), len(constraints), lstcpy, constraints)
        if (len(constraints_failed) < minimum):
            best_insertion_index = i
            minimum = len(constraints_failed)


    return best_insertion_index, minimum

def best_swap_index(indexOfWiz, lst, constraints, number_constraints_failed):
    lstcpy = lst[:]
    bestSwapIndex = -1
    minimum = number_constraints_failed
    for i in range(len(lst)):
        if (i == indexOfWiz):
            continue
        temp = lstcpy[indexOfWiz]
        lstcpy[indexOfWiz] = lstcpy[i]
        lstcpy[i] = temp

        constraints_failed, constraints_satisfied = validator(len(lstcpy), len(constraints), lstcpy, constraints)
        if (len(constraints_failed) < minimum):
            minimum = len(constraints_failed)
            bestSwapIndex = i
        temp = lstcpy[indexOfWiz]
        lstcpy[indexOfWiz] = lstcpy[i]
        lstcpy[i] = temp
    return bestSwapIndex, minimum


def parse_constraints(wizards, constraints):
    cMap = dict()
    wizset = set(wizards)
    for constraint in constraints:
        for wiz in constraint:
            if (wiz not in wizset):
                return
            elif (wiz in cMap):
                cMap[wiz].append(constraint)
            else:
                cMap[wiz] = [constraint]
    return cMap

def validator(num_wizards, num_constraints, output_lst, constraints):
    #output_ordering_set = set(output_lst)
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

""" =================================================================== """
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

    solution = solve(wizards, constraints)#left_fix_solve(num_wizards, num_constraints, wizards, constraints, args.input_file, args.output_file)
    write_output(args.output_file, solution)

    constraints_failed, constraints_satisfied = output_validator.main([args.input_file, args.output_file])
    end = time.clock()
    print("Total time = {}".format(end - start))
