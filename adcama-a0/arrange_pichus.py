#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Aditya Shekhar Camarushy adcama@iu.edu
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

def find_pichu_loc(house_map):
    return [(r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == 'p']

def horizontal_check(house_map,r,c):
    """
    For a given house map, checks if the row and column index corresponding to variables r,c is suitable in terms of the horizontal axis .ie.
    This function returns a boolean corresponding to whether the agent is susceptible to any attacks on the horizontal axis 
    """

    left_flag = True
    right_flag = True

    # Checking the left of selected position
    for i in range(c-1,-1,-1):
        if house_map[r][i] == 'p':
            left_flag = False
            break
        elif house_map[r][i] in 'X@':
            break
    
    # To avoid checking for the next sub-segment if it is already false
    if left_flag == False:
        return False

    # Checking the right of selected position
    for i in range(c+1,len(house_map[r])):
        if house_map[r][i] == 'p':
            right_flag = False
            break
        elif house_map[r][i] in 'X@':
            break
    
    return right_flag and left_flag

def vertical_check(house_map,r,c):

    """
    For a given house map, checks if the row and column index corresponding to variables r,c is suitable in terms of the vertical axis .ie.
    This function returns a boolean corresponding to whether the agent is susceptible to any attacks on the vertical axis 
    """

    above_flag = True
    below_flag = True

    # Checking above the selected position
    for i in range(r-1,-1,-1):
        if house_map[i][c] == 'p':
            above_flag = False
            break
        elif house_map[i][c] in 'X@':
            break
    
    # To avoid checking for the next sub-segment if it is already false
    if above_flag == False:
        return False

    # Checking below the selected position
    for i in range(r+1,len(house_map)):
        if house_map[i][c] == 'p':
            below_flag = False
            break
        elif house_map[r][c] in 'X@':
            break
    
    return above_flag and below_flag

def diagonal_check(house_map,r,c):

    """
    For a given house map, checks if the row and column index corresponding to variables r,c is suitable in terms of both the diagonals .ie.
    This function returns a boolean corresponding to whether the agent is susceptible to any attacks on either of the diagonals 
    """

    row_count = len(house_map)
    col_count = len(house_map[r])
    above_left_flag = above_right_flag = below_left_flag = below_right_flag = True

    # checking the diagonal that is above & left from our selected position
    r_ = r-1
    c_ = c-1

    while( r_ >= 0 and c_ >= 0 ):
        if house_map[r_][c_] == 'p':
            above_left_flag = False
            break
        elif house_map[r_][c_] in 'X@':
            break
        r_-=1
        c_-=1

    # checking the diagonal that is below & right from our selected position
    r_ = r+1
    c_ = c+1

    while( r_ < row_count and c_ < col_count ):
        if house_map[r_][c_] == 'p':
            below_right_flag = False
            break
        elif house_map[r_][c_] in 'X@':
            break
        r_+=1
        c_+=1

    # checking the diagonal that is above & right from our selected position 
    r_ = r-1
    c_ = c+1

    while( r_ >= 0 and c_ < col_count ):
        if house_map[r_][c_] == 'p':
            above_right_flag = False
            break
        elif house_map[r_][c_] in 'X@':
            break
        r_-=1
        c_+=1

    # checking the diagonal that is below & left from our selected position
    r_ = r+1
    c_ = c-1

    while( r_ < row_count and c_ >= 0 ):
        if house_map[r_][c_] == 'p':
            below_left_flag = False
            break
        elif house_map[r_][c_] in 'X@':
            break
        r_+=1
        c_-=1
    
    return above_left_flag and above_right_flag and below_left_flag and below_right_flag 

def safe_to_place(house_map,r,c):
    # This function returns the result of using 'AND' on all the booleans that are returned from function calls which check if the ROW & COLUMN & DIAGONALS corresponding to are safe for the agent or not 
    return horizontal_check(house_map,r,c) and vertical_check(house_map,r,c) and diagonal_check(house_map,r,c) 
        

# Get list of successors of given house_map state
def successors(house_map):
    # In addition to the given checks for the successor states I have incorporated a function called safe_to_place which returns a boolean to determine whether the position (r,c) is a suitable/unsuitable position to place an agent 
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' and safe_to_place(house_map, r, c)]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    fringe = [initial_house_map]
    while len(fringe) > 0:
        # using pop(0) so as to treat the list as a queue and perform BFS 
        for new_house_map in successors(fringe.pop(0)):
            if is_goal(new_house_map,k):
                return(new_house_map,True)
            fringe.append(new_house_map)
    return(new_house_map,False)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")


