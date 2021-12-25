#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Aditya Shekhar Camarushy adcama@iu.edu
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
         

# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

def reconstruct_path(source,destination,path_tracker):
        """
         This function retraces the path from the destination to the source i.e. the location from where pichu starts, this is done using a dictionary 'path_tracker' wherein the key is the current node and the value is the previous node.
         We then trace the path step by step and map each subsequent move to an alphabet corresponding to the direction i.e. U -> Up, D -> Down, R -> Right , L -> Left. We finally reverse the obtained path string and return it as the final path.   
        """
        cur = destination 
        final_str = '' 
        char = ''
        while True :
                if path_tracker[cur] != None:
                        prev = path_tracker[cur]
                        if cur[0]==prev[0] and cur[1]<prev[1]:
                                char = 'L'
                        elif cur[0]==prev[0] and cur[1]>prev[1]:
                                char = 'R'
                        elif cur[0]<prev[0] and cur[1]==prev[1]:
                                char = 'U'
                        elif cur[0]>prev[0] and cur[1]==prev[1]:
                                char = 'D'
                        cur = prev
                        final_str+=char
                        if cur == source:
                                break
        return final_str[::-1]



# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        fringe=[(pichu_loc,0)]

        # The following dictionary stores the previous node of each node encountered in the path
        prev_tracker = {}

        while fringe:
                # Removing the element at position 0 from the fringe 
                (curr_move, curr_dist)=fringe.pop(0)
                
                for move in moves(house_map, *curr_move):
                        # Adding the current position (popped out from fringe) as the previous move of the new move that we are analysing 
                        prev_tracker[move] = curr_move

                        if house_map[move[0]][move[1]]=="@":

                                # Reconstructing the final path from source to destination
                                path_str = reconstruct_path(pichu_loc,move,prev_tracker) 

                                # Return the answer in terms of the distance and path followed
                                return (curr_dist+1, path_str)  
                        else:
                                fringe.append((move, curr_dist + 1))

                                # mark the node as visited by setting the character as " V ", this is to prevent re-visting the same nodes over again 
                                house_map[move[0]][move[1]] = "V" 
        return (-1,'')

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])


