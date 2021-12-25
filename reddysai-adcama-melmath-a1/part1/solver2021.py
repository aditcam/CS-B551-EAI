#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Sai Prajwal Reddy: reddysai@iu.edu, Aditya Camarushy: adcama@iu.edu, Melissa Rochelle Mathias: melmath@iu.edu
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

from os import stat
import sys
from typing import Counter
import copy
import time

ROWS=5
COLS=5

# Only The below class was structured using the following article as reference, the implementation search technique however was not devised using this article .
# article link : https://towardsdatascience.com/a-star-a-search-algorithm-eb495fb156bb

# Implementation of the A* search was done using this article as reference, absolute : https://www.geeksforgeeks.org/a-search-algorithm/#:~:text=What%20A*%20Search%20Algorithm%20does,and%20process%20that%20node%2Fcell. 
class State:
    def __init__(self,board = None, move = None):
        self.board = board
        self.parent = None
        self.path_to_state = []
        self.move = move
        self.g = 0
        self.h = self.heuristic(self.board)
        self.f = 0

    # overriding the lt dunder method so as to make comparision of State objects easier using this reference : https://www.pythonpool.com/python-__lt__/
    # def __lt__(self,other):
    #     return self.f<other.f and self.board == other.board

    def __eq__(self,other):
        return self.f>other.f and self.board == other.board

    # overriding the hash dunder method so as to make hashing of State objects easier using these references :https://www.kite.com/python/answers/how-to-use-a-custom-object-as-a-key-in-a-dictionary-in-python
    # https://eng.lyft.com/hashing-and-equality-in-python-2ea8c738fb9d
    # def __hash__(self):
    #     return hash((tuple(map(tuple,self.board))))

    # def __contains__(self,other):
    #     for x in other:
    #         if x.board == self.board and x.f < self.f:
    #             return True
    #     return False 
    
    def precompute_heuristic(self):

        start_arr = [[0,1,2,2,1],[1,2,3,3,2],[2,3,4,4,3],[2,3,4,4,3],[1,2,3,3,2]]

        def left_loop_col(arr):
            result = copy.deepcopy(arr)
            for row in result:
                row.insert(0,row.pop())
            return result
        
        def bottom_loop_row(arr):
            result = copy.deepcopy(arr)
            result.insert(0,result.pop())
            return result

        heuristic_dict = {}
        heuristic_dict[1] = start_arr 
        temp_arr = copy.deepcopy(start_arr)
        for i in range(2,26):
            temp_arr = left_loop_col(temp_arr)
            if i%5 == 1:
                temp_arr = bottom_loop_row(temp_arr)
            heuristic_dict[i] = temp_arr

        return heuristic_dict

    def heuristic(self,state):
        def flattening(state):
            return [j for i in state for j in i]
        flattened_state = flattening(state)
        result = 0
        for i in range(len(flattened_state)):
            if i+1 != flattened_state[i]:
                result+=1
        return result

        # heuristic_dict = self.precompute_heuristic()
        
        # result = 0

        # for i in range(5):
        #     for j in range(5):
        #         result += heuristic_dict[state[i][j]][i][j]
        # return result/16

    def set_f(self):
        self.f = self.g + self.h
       
def print_board(board):
    for i in range(5):
        for j in range(5):
            print(board[i][j],"\t",end="")
        print("")

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

def board_two_dimensional(state):
    return [ x for x in (list(state[y*5:(y+1)*5]) for y in range(5))]


#function for moving the row in left and right

def row_states(state):

    #stores the successors of the row up and down combinations
    row_succ = {}
   
    #row to the right
    for i in range (0,ROWS): 
        new_state = copy.deepcopy(state)
        new_state[i].insert(0,new_state[i].pop())
        row_succ['R'+str((i+1))] = new_state

    #row to the left
    for i in range(0, ROWS):
        new_state = copy.deepcopy(state)
        new_state[i].insert(len(new_state[i]),new_state[i].pop(0))
        row_succ['L'+str((i+1))] = new_state
       
    return row_succ

# create column states
def column_states(state):
    col_succ = {}
    
    #For columns moving up
    for i in range(0,COLS):
        new_state = copy.deepcopy(state)
        for j in range(0,ROWS):
            if j == ROWS-1:
                new_state[j][i] = state[0][i]
                col_succ['U'+str(i+1)] = new_state
            else:
                new_state[j][i] = state[j+1][i]

    #For columns moving down
    for i in range(0,COLS):
        new_state = copy.deepcopy(state)
        for j in range(0,ROWS):
            if j == 0:
                new_state[j][i] = state[-1][i]
            else:
                new_state[j][i] = state[j-1][i]
        col_succ['D'+str(i+1)] = new_state
    return col_succ 


# return a list of possible rotations states
def rotation_states(state):
    def outer_rotation(state,dir):

        state = copy.deepcopy(state)
        outer_ring = []

        # Getting all the elements in the outer ring
        # We referenced this link to understand the extend() method which can be used to concatenate multiple lists into a single list: https://www.w3schools.com/python/ref_list_extend.asp
        outer_ring.extend(list(state[0][i] for i in range(5)))  
        outer_ring.extend(list(state[i][4] for i in range(1,5)))
        outer_ring.extend(list(state[4][i] for i in range(3,-1,-1)))
        outer_ring.extend(list(state[i][0] for i in range(3,0,-1)))

        if dir =='c':
            # Shifting the elements by an index 
            outer_ring.insert(0,outer_ring.pop())
        elif dir == 'cc':
            outer_ring.insert(len(outer_ring),outer_ring.pop(0))
        
        # Assigning the shifted values to the outer 
        state[0] = outer_ring[:5]
        counter=5

        for i in range(1,5):
            state[i][4] = outer_ring[counter]
            counter+=1
        
        for i in range(3,-1,-1):
            state[4][i] = outer_ring[counter]
            counter+=1
        
        for i in range(3,0,-1):
            state[i][0] = outer_ring[counter]
            counter+=1
        
        return state

    def inner_rotation(state,dir):

        state = copy.deepcopy(state) # We referred to this link to understand the concept of a deep copy in Python : https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/
        inner_ring = []

        # Getting all the elements in the outer ring
        inner_ring.extend(list(state[1][i] for i in range(1,4)))
        inner_ring.extend(list(state[i][3] for i in range(2,4)))
        inner_ring.extend(list(state[3][i] for i in range(2,0,-1)))
        inner_ring.extend(list(state[i][1] for i in range(2,1,-1)))

        if dir =='c':
            # Shifting the elements by an index 
            inner_ring.insert(0,inner_ring.pop())
        elif dir == 'cc':
            inner_ring.insert(len(inner_ring),inner_ring.pop(0))
        
        counter = 0
        # Assigning the shifted values to the outer 
        for i in range(1,4):
            state[1][i] = inner_ring[counter]
            counter+=1

        for i in range(2,4):
            state[i][3] = inner_ring[counter]
            counter+=1
        
        for i in range(2,0,-1):
            state[3][i] = inner_ring[counter]
            counter+=1
        
        for i in range(2,1,-1):
            state[i][1] = inner_ring[counter]
            counter+=1
        
        return state

    return {'Oc':outer_rotation(state,'c'),'Occ':outer_rotation(state,'cc'),'Ic':inner_rotation(state,'c'),'Icc':inner_rotation(state,'cc')}

# return a list of possible successor states
def successors(state):
    output_dict = {}
    # We referred to this link https://stackoverflow.com/questions/1781571/how-to-concatenate-two-dictionaries-to-create-a-new-one-in-python to understand the working of dictionary concatenation
    output_dict.update(rotation_states(state)) 
    output_dict.update(row_states(state))
    output_dict.update(column_states(state))
    output_lst = [] # A list of objects belonging to state class will be stored in this list and returned

    for key,value in output_dict.items():
        output_lst.append(State(value,key))

    return output_lst

# check if we've reached the goal
def is_goal(state):
    state_arr = [j for i in state.board for j in i]
    goal_arr = [i for i in range(1,26)]
    return state_arr == goal_arr

def solve(initial_board):
    board = board_two_dimensional(initial_board)
    pq = [] # initialize priority queue
    visited_dict = {}

    # initial states set-up before performing the search algorithm
    for state in successors(board):
        state.path_to_state = [state.move]
        state.g = 1
        state.set_f()
        pq.append(state)
    pq.sort(key=lambda x:x.f)
    if is_goal(pq[0]):
        return pq[0].path_to_state
    # The below block is just to check the outputs of the inital states generated
    # for i in pq:
    #     print("Board is -")
    #     print_board(i.board)
    #     print("Path to State:{} Move:{} g:{} h:{} f:{}".format(i.path_to_state,i.move,i.g,i.h,i.f))
    #     print("------------------------------------------------------------------------------")
    # print_board(board)
    # print("------------------------------------------------------------------------------")
    
    tc = 0
    i = 0
    start = end = None
    start = time.time()
    while pq:
        i+=1
        exploration_state = pq.pop(0)
        if is_goal(exploration_state):
            end = time.time()
            print(end-start)
            # print(tc)
            print(i)
            print(len(pq))
            return exploration_state.path_to_state
        
        successor_states = successors(exploration_state.board)

        # print_board(exploration_state.board)
        # print("Path to State:{} Move:{} g:{} h:{} f:{}".format(exploration_state.path_to_state,exploration_state.move,exploration_state.g,exploration_state.h,exploration_state.f))
        # print(len(successor_states))
        
        for state in successor_states:
            # print("Path to State:{} Move:{} g:{} h:{} f:{}".format(exploration_state.path_to_state,exploration_state.move,exploration_state.g,exploration_state.h,exploration_state.f))
            # print_board(state.board)
            state.parent = exploration_state
            state.path_to_state = exploration_state.path_to_state + [state.move]
            state.g = exploration_state.g+1
            state.set_f()
            # print("Path to State:{} Move:{} g:{} h:{} f:{}".format(state.path_to_state,state.move,state.g,state.h,state.f))
            # print_board(state.board)

        # start = time.time()
        j=0
        for state in successor_states:

            # bool_val = False

            # for x in pq:
            #     if state.board == x.board and state.f > x.f:
            #         bool_val = True
            #         break

            if state in pq:
                continue
            elif hash((tuple(map(tuple,state.board)))) in visited_dict and visited_dict[hash((tuple(map(tuple,state.board))))] < state.f:
                continue
            else :
                pq.append(state)
                # print(len(pq))
        pq.sort(key=lambda x:x.f)
        # end = time.time()
        # tc += end-start
        # visited_list.append(exploration_state)]
        visited_dict[hash((tuple(map(tuple,exploration_state.board))))] = exploration_state.f
        



    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    # print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    # print(board_two_dimensional(tuple(start_state)))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
