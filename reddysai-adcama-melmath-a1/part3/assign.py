#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Sai Prajwal Reddy: reddysai@iu.edu, Aditya Camarushy: adcama@iu.edu, Melissa Rochelle Mathias: melmath@iu.edu
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time
from typing import final
import copy
import random

def beautify_groups(state):
    output = []
    for group in state:
        # The below technique was referenced from : https://www.geeksforgeeks.org/python-program-to-concatenate-all-elements-of-a-list-into-a-string/
        output.append('-'.join(group)) 
    return output

def time_cost(state,student_preferences):
    
    # Cost for each group 
    final_cost = len(state) * 5
    
    for group in state:
            for student in group:
                # print(student)
                # Cost for different group size
                if student_preferences[student]["req_size"] != len(group):
                    # print(2)
                    final_cost += 2

                # Cost for students assigned to groups with avoid individuals
                for avoid_student in student_preferences[student]["avoid"]:
                    if avoid_student in group:
                        # print(10)
                        final_cost += 10

                # Cost for student not assigned to person they requested to work with
                for student_partner in student_preferences[student]["group"]:
                    if student_partner == 'xxx' or student_partner == 'zzz':
                        continue
                    else:
                        if student_partner == student:
                            continue
                        else:
                            if student_partner not in group:
                                # print(3)
                                final_cost += 0.05 * 60
    
    return final_cost

def generate_random(student):
    result = []
    while student:
        size = random.randint(1,3)
        # print(size)
        if size <= len(student):
            group = random.sample(student,size)
            student = [x for x in student if x not in group]
            result.append(group)
        else:
             continue
    # print("Random state " , result)
    return result

def best_successor(state,student_preferences,visited_states):
    min_cost = 999999999
    temp_state = copy.deepcopy(state)
    best_state = None
    for i in range(len(state)):
        for j in range(len(state[i])):
            for k in range(len(state)):
                if k != i:

                    # print(temp_state)
                    # moving a student by 1 position
                    temp_state = copy.deepcopy(state)
                    temp_state[k].append(state[i][j])
                    value = temp_state[i].pop(j)

                    # delete empty columns
                    temp_state = [x for x in temp_state if x]
                    
                    if temp_state not in visited_states:
                    # compute cost 
                        new_state_cost = time_cost(temp_state,student_preferences)
                        # print((temp_state))
                        
                        visited_states.append(temp_state)

                        if new_state_cost < min_cost:
                            # print(new_state_cost)
                            min_cost = new_state_cost
                            best_state = copy.deepcopy(temp_state)
                    
                    del temp_state

    return {"assigned-groups":best_state,"total-cost":min_cost}


def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    student_preferences = {}
    # The code for file operations was referenced from https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
    with open(input_file) as fp:
        lines = fp.readlines()
        for line in lines:
            username,group,avoid = line.split()
            group = group.split('-')
            avoid = avoid.split(',')
            if avoid[0] == '_':
                avoid = []
            student_preferences[username] = {"group":group,"avoid":avoid,"req_size":len(group)}
        # print(student_preferences)
    
    # Dictionary for student allocation status (to any group, 0 if not in any group, otherwise 1)
    student_allocation = {}
    for key in student_preferences.keys():
        student_allocation[key] = 0

    # Creating a starting state that is the best possible to begin with 
    # start_state = []
    # i = 0
    # for key,values in student_preferences.items():
    #     if student_allocation[key] == 1:
    #         continue
    #     else:
    #         start_state.append([])
    #         start_state[i].append(key)
    #         student_allocation[key] = 1
    #         # print(student_allocation)
    #         for student in values['group']:
    #             if student == 'xxx' or 'zzz' :
    #                 # Sorting a dictionary based on keys (in the line below) using the following reference : https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    #                 # sorted(student_allocation,key = student_allocation.get)
    #                 for student_ in [x for x in student_allocation.keys() if student_allocation[x] != 1]:
    #                     if key not in student_preferences[student_]["avoid"] and student_preferences[student_]["req_size"] == student_preferences[key]["req_size"]: # perhaps removing the req_size is a better option ? 
    #                         start_state[i].append(student_)
    #                         student_allocation[student_] = 1
    #                         # print(student_allocation)

    #             else :
    #                 if student == key or student_allocation[student] == 1:
    #                     continue
    #                 elif student_allocation[student] == 0:
    #                     if key not in student_preferences[student]['avoid']:
    #                         start_state[i].append(student)
    #                         student_allocation[student] = 1
    #                         # print(student_allocation)
    #         i+=1
    # print(start_state)
    # result_dict = {"assigned-groups":start_state,"total-cost":time_cost(start_state,student_preferences)}
    # print(result_dict)

    # start_state = [['djcran'], ['sahmaini'], ['nthakurd'], ['fanjun'], ['vkvats'], ['sulagaop']]
    # result_dict = {"assigned-groups":start_state,"total-cost":time_cost(start_state,student_preferences)}
    # visited_states = [start_state]
    # current_best = result_dict
    # print(time_cost(['djcran-vkvats-sahmaini', '', 'sulagaop', 'fanjun', 'nthakurd'],student_preferences))

    # Generate Random start states
    global_best = {'assigned-groups':None,'total-cost':99999999}
    while True:
        start_state = generate_random([x for x in student_preferences.keys()])
        current_best = {'assigned-groups':start_state,'total-cost':time_cost(start_state,student_preferences)}
        visited_states = [current_best]
        # print(current_best)
        while True:
            next_state = best_successor(current_best['assigned-groups'],student_preferences,visited_states)
            if next_state['total-cost'] < current_best['total-cost']:
                current_best = next_state
                # temp_op = copy.deepcopy(current_best)
                # temp_op['assigned-groups'] = beautify_groups(temp_op['assigned-groups'])
                # yield temp_op
            else :
                current_best['assigned-groups'] = beautify_groups(current_best['assigned-groups'])
                if current_best['total-cost'] < global_best['total-cost']:
                    global_best = copy.deepcopy(current_best)
                    yield current_best
                break

    """
    # Simple example. First we yield a quick solution
    yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12", "vrmath"],
               "total-cost" : 12})

    # Then we think a while and return another solution:
    time.sleep(10)
    yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12-vrmath"],
               "total-cost" : 10})

    # This solution will never befound, but that's ok; program will be killed eventually by the
    #  test script.
    while True:
        pass
    
    yield({"assigned-groups": ["vibvats-djcran", "zkachwal-shah12-vrmath"],
               "total-cost" : 9})
    """

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])

    solver(sys.argv[1])
