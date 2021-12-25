#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
# Aditya Shekhar Camarushy : adcama
# Melissa Rochelle Mathias : melmath
# Sai Prajwal reddy : saireddy 
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
from copy import deepcopy

# class board:
#     def __init__(self,parent,level,score,board_state):
#         self.parent = parent
#         self.level = level
#         self.score = score
#         self.board_state = board_state
#         self.hash_val = hash(str(self.board_state))

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def board_two_dimensional(state,N):
    # Code to convert a list of elements into a 2d list
    return [ x for x in (list(state[y*N:(y+1)*N]) for y in range(N))]

def flatten_board(state):
    # Code to flatten a 2D List
            return [j for i in state for j in i]

def immediate_surrounding_score(board,N,row,col):
    score = 0
    piece = board[row][col]
    if not in_board(row-1,col-1,N):
        score+=0.1
    if not in_board(row-1,col,N):
        score+=0.1
    if not in_board(row-1,col+1,N):
        score+=0.1
    if not in_board(row,col+1,N):
        score+=0.1
    if not in_board(row+1,col+1,N):
        score+=0.1
    if not in_board(row+1,col,N):
        score+=0.1
    if not in_board(row+1,col-1,N):
        score+=0.1
    if not in_board(row,col-1,N):
        score+=0.1
        
 
    if piece in 'Ww@':
        
        if in_board(row-1,col-1,N):
            if board[row-1][col-1] in 'Ww@':
                score+=0.2
            elif board[row-1][col-1] in 'Bb$':
                score-=0.1
            else:
                score += 0
        
        if in_board(row-1,col,N):
            if board[row-1][col] in 'Ww@':
                score+=0.2
            elif board[row-1][col] in 'Bb$':
                score-=0.1
            else:
                score += 0
        
        if in_board(row-1,col+1,N):
            if board[row-1][col+1] in 'Ww@':
                score+=0.2
            elif board[row-1][col+1] in 'Bb$':
                score-=0.1
            else:
                score+=0
        
        if in_board(row,col+1,N):
            if board[row][col+1] in 'Ww@':
                score+=0.2
            elif board[row][col+1] in 'Bb$':
                score-=0.1
            else:
                score+=0
        
        if in_board(row+1,col+1,N):
            if board[row+1][col+1] in 'Ww@':
                score+=0.2
            elif board[row+1][col+1] in 'Bb$':
                score-=0.1
            else:
                score += 0
        
        if in_board(row+1,col,N):
            if board[row+1][col] in 'Ww@':
                score+=0.2
            elif board[row+1][col] in 'Bb$':
                score-=0.1
            else:
                score += 0
        
        if in_board(row+1,col-1,N):
            if board[row+1][col-1] in 'Ww@':
                score+=0.2
            elif board[row+1][col-1] in 'Bb$':
                score-=0.1
            else:
                score += 0
        
        if in_board(row,col-1,N):
            if board[row][col-1] in 'Ww@':
                score+=0.2
            elif board[row][col-1] in 'Bb$':
                score-=0.1
            else:
                score += 0
    

    elif piece in 'Bb$':
        if in_board(row-1,col-1,N):
            if board[row-1][col-1] in 'Bb$':
                score+=0.2
            elif board[row-1][col-1] in 'Ww@':
                score-=0.1
            else:
                score+=0

        if in_board(row-1,col,N): 
            if board[row-1][col] in 'Bb$':
                score+=0.2
            elif board[row-1][col] in 'Ww@':
                score-=0.1
            else:
                score += 0

        if in_board(row-1,col+1,N):
            if board[row-1][col+1] in 'Bb$':
                score+=0.2
            elif board[row-1][col+1] in 'Ww@':
                score-=0.1
            else:
                score += 0
        
        if in_board(row,col+1,N):
            if board[row][col+1] in 'Bb$':
                score+=0.2
            elif board[row][col+1] in 'Ww@':
                score-=0.1
            else:
                score += 0
        
        if in_board(row+1,col+1,N):
        
            if board[row+1][col+1] in 'Bb$':
                score+=0.2
            elif board[row+1][col+1] in 'Ww@':
                score-=0.1
            else:
                score += 0
        
        if in_board(row+1,col,N):
            if board[row+1][col] in 'Bb$':
                score+=0.2
            elif board[row+1][col] in 'Ww@':
                score-=0.1
            else:
                score += 0
        
        if in_board(row+1,col-1,N):
            if board[row+1][col-1] in 'Bb$':
                score+=0.2
            elif board[row+1][col-1] in 'Ww@':
                score-=0.1
            else:
                score += 0
                
        if in_board(row,col-1,N):
            if board[row][col-1] in 'Bb$':
                score+=0.2
            elif board[row][col-1] in 'Ww@':
                score-=0.1
            else:
                score += 0
 

    if piece in 'Ww@':
        return score
    elif piece in 'Bb$':
        return -score

def board_score(board,N):
    score = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] != '.':
                score = score + immediate_surrounding_score(board,N,i,j)
    flat_board = flatten_board(board)
    score_metric  = {'.':0,'W':3,'w':2,'@':8,'B':-3,'b':-2,'$':-8}
    for char in flat_board:
        score+=score_metric[char]
    return score

def in_board(x,y,N):
    # Function to check if the given coordinates are on the board
    if (x<N and x>=0) and (y<N and y>=0):
        return True
    return False

def pichu_succ(board,N,row,col):
    '''
    row : row coordinate of pichu
    col : col coordinate of pichu
    '''
    board_list = []
    # Moves for the white
    if board[row][col] == 'w':
        temp_board = None
        # Checking the bottom left of the pichu
        if in_board(row+1,col-1,N):
            if board[row+1][col-1] == '.':
                temp_board = deepcopy(board)
                temp_board[row+1][col-1] = 'w'
                if row+1 == N-1:
                    temp_board[row+1][col-1] = '@'
                temp_board[row][col] = '.'
            elif board[row+1][col-1] == 'b' and in_board(row+2,col-2,N) and board[row+2][col-2] == '.' :
                temp_board = deepcopy(board)
                temp_board[row+2][col-2] = 'w'
                if row+2 == N-1:
                    temp_board[row+2][col-2] = '@'
                temp_board[row][col] = '.'
                temp_board[row+1][col-1] = '.'
        if temp_board:
            board_list.append(temp_board)
        temp_board = None

        # Checking the bottom right of the pichu
        if in_board(row+1,col+1,N):
            if board[row+1][col+1] == '.':
                temp_board = deepcopy(board)
                temp_board[row+1][col+1] = 'w'
                if row+1 == N-1:
                    temp_board[row+1][col+1] = '@'
                temp_board[row][col] = '.'
            elif board[row+1][col+1] == 'b' and in_board(row+2,col+2,N) and board[row+2][col+2] == '.' :
                temp_board = deepcopy(board)
                temp_board[row+2][col+2] = 'w'
                if row+2 == N-1:
                    temp_board[row+2][col+2] = '@'
                temp_board[row][col] = '.'
                temp_board[row+1][col+1] = '.'
        if temp_board:
            board_list.append(temp_board)
        temp_board = None

    # Moves for the black
    if board[row][col] == 'b':
        temp_board = None
        # Checking the top left of the pichu
        if in_board(row-1,col-1,N):
            if board[row-1][col-1] == '.':
                temp_board = deepcopy(board)
                temp_board[row-1][col-1] = 'b'
                if row-1 == 0:
                    temp_board[row-1][col-1] = '$'
                temp_board[row][col] = '.'
            elif board[row-1][col-1] == 'w' and in_board(row-2,col-2,N) and board[row-2][col-2] == '.':
                temp_board = deepcopy(board)
                temp_board[row-2][col-2] = 'b'
                if row-2 == 0:
                    temp_board[row-2][col-2] = '$'
                temp_board[row][col] = '.'
                temp_board[row-1][col-1] = '.'
        if temp_board:
            board_list.append(temp_board)
        temp_board = None

        # Checking the top right of the pichu
        if in_board(row-1,col+1,N):
            if board[row-1][col+1] == '.':
                temp_board = deepcopy(board)
                temp_board[row-1][col+1] = 'b'
                if row-1 == 0:
                    temp_board[row-1][col+1] = '$'
                temp_board[row][col] = '.'
            elif board[row-1][col+1] == 'w' and in_board(row-2,col+2,N) and board[row-2][col+2] == '.':
                temp_board = deepcopy(board)
                temp_board[row-2][col+2] = 'b'
                if row-1 == 0:
                    temp_board[row-2][col+2] = '$'
                temp_board[row][col] = '.'
                temp_board[row-1][col+1] = '.'
        if temp_board:
            board_list.append(temp_board)
        temp_board = None
        
    return board_list

def pikachu_succ(board,N,row,col):


    '''
    row : row coordinate of pikachu
    col : col coordinate of pikachu
    '''
    board_list = []
    # Moves for the white
    if board[row][col] == 'W':
        temp_board = None
        # Considering 1 and 2 step moves to the left 
        if in_board(row,col-1,N):
            # if 1 step left is empty 
            if board[row][col-1]=='.':
                temp_board = deepcopy(board)
                temp_board[row][col-1] = 'W'
                temp_board[row][col] = '.'
                board_list.append(temp_board)
                
            elif board[row][col-1] in 'Bb' and in_board(row,col-2,N) and board[row][col-2] == '.':
                temp_board = deepcopy(board)
                temp_board[row][col-2] = 'W'
                temp_board[row][col] = '.'
                temp_board[row][col-1] = '.'
                board_list.append(temp_board)
                
            if in_board(row,col-2,N):
                # if 2 step left is empty 
                if board[row][col-2] == '.' and board[row][col-1] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row][col-2] = 'W'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)

                elif board[row][col-2] in 'Bb' and board[row][col-1] == '.' and in_board(row,col-3,N) and board[row][col-3] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row][col-3] = 'W'
                    temp_board[row][col] = '.'
                    temp_board[row][col-2] = '.'
                    board_list.append(temp_board)
                    
        # Considering 1 and 2 step moves to the right 
        if in_board(row,col+1,N):
            # if 1 step right is empty 
            if board[row][col+1]=='.':
                temp_board = deepcopy(board)
                temp_board[row][col+1] = 'W'
                temp_board[row][col] = '.'
                board_list.append(temp_board)
                
            elif board[row][col+1] in 'Bb' and in_board(row,col+2,N) and board[row][col+2] == '.':
                temp_board = deepcopy(board)
                temp_board[row][col+2] = 'W'
                temp_board[row][col] = '.'
                temp_board[row][col+1] = '.'
                board_list.append(temp_board)
                
            if in_board(row,col+2,N):
                # if 2 step right is empty 
                if board[row][col+2] == '.' and board[row][col+1] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row][col+2] = 'W'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)

                elif board[row][col+2] in 'Bb' and board[row][col+1] == '.' and in_board(row,col+3,N) and board[row][col+3] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row][col+3] = 'W'
                    temp_board[row][col] = '.'
                    temp_board[row][col+2] = '.'
                    board_list.append(temp_board)
                    
        # Considering 1 and 2 step moves forward
        if in_board(row+1,col,N):
            # if 1 step right is empty 
            if board[row+1][col]=='.':
                temp_board = deepcopy(board)
                temp_board[row+1][col] = 'W'
                if row+1 == N-1:
                    temp_board[row+1][col] = '@'
                temp_board[row][col] = '.'
                board_list.append(temp_board)
                
            elif board[row+1][col] in 'Bb' and in_board(row+2,col,N) and board[row+2][col] == '.':
                temp_board = deepcopy(board)
                temp_board[row+2][col] = 'W'
                if row+2 == N-1:
                    temp_board[row+2][col] = '@'
                temp_board[row][col] = '.'
                temp_board[row+1][col] = '.'
                board_list.append(temp_board)
                
            if in_board(row+2,col,N):
                # if 2 step right is empty 
                if board[row+2][col] == '.' and board[row+1][col] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row+2][col] = 'W'
                    if row+2 == N-1:
                        temp_board[row+2][col] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)

                elif board[row+2][col] in 'Bb' and board[row+1][col] == '.' and in_board(row+3,col,N) and board[row+3][col] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row+3][col] = 'W'
                    if row+3 == N-1:
                        temp_board[row+3][col] = '@'
                    temp_board[row][col] = '.'
                    temp_board[row+2][col] = '.'
                    board_list.append(temp_board)  
                    
                    
        # Moves for the black
    if board[row][col] == 'B':
        temp_board = None
        # Considering 1 and 2 step moves to the left 
        if in_board(row,col-1,N):
            # if 1 step left is empty 
            if board[row][col-1]=='.':
                temp_board = deepcopy(board)
                temp_board[row][col-1] = 'B'
                temp_board[row][col] = '.'
                board_list.append(temp_board)
                
            elif board[row][col-1] in 'Ww' and in_board(row,col-2,N) and board[row][col-2] == '.':
                temp_board = deepcopy(board)
                temp_board[row][col-2] = 'B'
                temp_board[row][col] = '.'
                temp_board[row][col-1] = '.'
                board_list.append(temp_board)
                
            if in_board(row,col-2,N):
                # if 2 step left is emapty 
                if board[row][col-2] == '.' and board[row][col-1] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row][col-2] = 'B'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)

                elif board[row][col-2] in 'Ww' and board[row][col-1] == '.' and in_board(row,col-3,N) and board[row][col-3] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row][col-3] = 'B'
                    temp_board[row][col] = '.'
                    temp_board[row][col-2] = '.'
                    board_list.append(temp_board)
                    
        # Considering 1 and 2 step moves to the right 
        if in_board(row,col+1,N):
            # if 1 step right is empty 
            if board[row][col+1]=='.':
                temp_board = deepcopy(board)
                temp_board[row][col+1] = 'B'
                temp_board[row][col] = '.'
                board_list.append(temp_board)
                
            elif board[row][col+1] in 'Ww' and in_board(row,col+2,N) and board[row][col+2] == '.':
                temp_board = deepcopy(board)
                temp_board[row][col+2] = 'B'
                temp_board[row][col] = '.'
                temp_board[row][col+1] = '.'
                board_list.append(temp_board)
                
            if in_board(row,col+2,N):
                # if 2 steps right is empty 
                if board[row][col+2] == '.' and board[row][col+1] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row][col+2] = 'B'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)

                elif board[row][col+2] in 'Ww' and board[row][col+1] == '.' and in_board(row,col+3,N) and board[row][col+3] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row][col+3] = 'B'
                    temp_board[row][col] = '.'
                    temp_board[row][col+2] = '.'
                    board_list.append(temp_board)
                    
        # Considering 1 and 2 step moves forward
        if in_board(row-1,col,N):
            # if 1 step forward is empty 
            if board[row-1][col]=='.':
                temp_board = deepcopy(board)
                temp_board[row-1][col] = 'B'
                if row-1 == 0:
                    temp_board[row-1][col] = '$'
                temp_board[row][col] = '.'
                board_list.append(temp_board)
                
            elif board[row-1][col] in 'Ww' and in_board(row-2,col,N) and board[row-2][col] == '.':
                temp_board = deepcopy(board)
                temp_board[row-2][col] = 'B'
                if row-2 == 0:
                    temp_board[row-2][col] = '$'
                temp_board[row][col] = '.'
                temp_board[row-1][col] = '.'
                board_list.append(temp_board)
                
            if in_board(row-2,col,N):
                # if 2 steps forward is empty 
                if board[row-2][col] == '.' and board[row-1][col] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row-2][col] = 'B'
                    if row-2 == 0:
                        temp_board[row-2][col] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)

                elif board[row-2][col] in 'Ww' and board[row-1][col] == '.' and in_board(row-3,col,N) and board[row-3][col] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row-3][col] = 'B'
                    if row-3 == 0:
                        temp_board[row-3][col] = '$'
                    temp_board[row][col] = '.'
                    temp_board[row-2][col] = '.'
                    board_list.append(temp_board)
                    
    return board_list     


    '''
    row : row of raichu
    col : col of raichu
    '''
    board_list = []
    # Moves for the white raichu 
    if board[row][col] == '@':
        temp_board = None    
     # Considering moves to the left
        for j in range(1,col+1):
            if in_board(row,col-j,N):
                if board[row][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row][col-j] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row][col-j] in 'Ww@':
                    break

                elif board[row][col-j] in 'Bb$' and in_board(row,col-(j+1),N) and board[row][col-(j+1)] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row][col-(j+1)] = '@'
                    temp_board[row][col] = '.'
                    temp_board[row][col-j] = '.'
                    board_list.append(temp_board)
                    break
                    
                elif board[row][col-j] in 'Bb$' and in_board(row,col-(j+1),N) and board[row][col-(j+1)] != '.' :
                    break 
                # Considering moves to the right 
        j=1
        while in_board(row,col+j,N):
            if board[row][col+j]=='.':
                temp_board = deepcopy(board)
                temp_board[row][col+j] = '@'
                temp_board[row][col] = '.'
                board_list.append(temp_board)
                
            elif board[row][col+j] in 'Ww@':
                break

            elif board[row][col+j] in 'Bb$' and in_board(row,col+(j+1),N) and board[row][col+(j+1)] == '.':
                temp_board = deepcopy(board)
                temp_board[row][col+(j+1)] = '@'
                temp_board[row][col] = '.'
                temp_board[row][col+j] = '.'
                board_list.append(temp_board)
                break
            
            
            elif board[row][col+j] in 'Bb$' and in_board(row,col+(j+1),N) and board[row][col+(j+1)] != '.':
                break
            
            j+=1

        # Considering moves to forward
        for j in range(1,N):
            if in_board(row+j,col,N):
                if board[row+j][col]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row+j][col] in 'Ww@':
                    break
                
                elif board[row+j][col] in 'Bb$' and in_board(row+(j+1),col,N) and board[row+(j+1)][col] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row+(j+1)][col] = '@'
                    temp_board[row][col] = '.'
                    temp_board[row+j][col] = '.'
                    board_list.append(temp_board)
                    break
                
                elif board[row+j][col] in 'Bb$' and in_board(row+(j+1),col,N) and board[row+(j+1)][col] != '.' :
                    break

        # Considering moves to backwards
        for j in range(1,N):
            if in_board(row-j,col,N):
                if board[row-j][col]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col] in 'Ww@':
                    break

                elif board[row-j][col] in 'Bb$' and in_board(row-(j+1),col,N) and board[row-(j+1)][col] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row-(j+1)][col] = '@'
                    temp_board[row][col] = '.'
                    temp_board[row-j][col] = '.'
                    board_list.append(temp_board)
                    break
                    
                elif board[row-j][col] in 'Bb$' and in_board(row-(j+1),col,N) and board[row-(j+1)][col] != '.' :
                    break
                
        # Considering moves to right diagonal downwards
        for j in range(1,N):
            if in_board(row+j,col+j,N):
                if board[row+j][col+j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col+j] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row+j][col+j] in 'Ww@':
                    break

                elif board[row+j][col+j] in 'Bb$' and in_board(row+(j+1),col+(j+1),N) and board[row+(j+1)][col+(j+1)] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row+(j+1)][col+(j+1)] = '@'
                    temp_board[row][col] = '.'
                    temp_board[row+j][col+j] = '.'
                    board_list.append(temp_board)
                    break
                    
                elif board[row+j][col+j] in 'Bb$' and in_board(row+(j+1),col+(j+1),N) and board[row+(j+1)][col+(j+1)] != '.' :
                    break
                 

        # Considering moves to right diagonal upwards
        for j in range(1,N):
            if in_board(row-j,col+j,N):
                if board[row-j][col+j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col+j] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col+j] in 'Ww@':
                    break

                elif board[row-j][col+j] in 'Bb$' and in_board(row-(j+1),col+(j+1),N) and board[row-(j+1)][col+(j+1)] == '.' :
                    temp_board = deepcopy(board)
                    # print_brd(temp_board)
                    # print("j:",j)
                    # print("element :"+str(board[row][col]))
                    # print("Top right :"+str(board[row-j][col+j]))
                    # print("Top Right :"+str(board[row-j-1][col+j+1]))
                    temp_board[row-(j+1)][col+(j+1)] = '@'
                    temp_board[row][col] = '.'
                    temp_board[row-j][col+j] = '.'
                    board_list.append(temp_board)
                    break
                    
                elif board[row-j][col+j] in 'Bb$' and in_board(row-(j+1),col+(j+1),N) and board[row-(j+1)][col+(j+1)] != '.':
                    break

        # Considering moves to left diagonal downwards
        for j in range(1,N):
            if in_board(row+j,col-j,N):
                if board[row+j][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col-j] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row+j][col-j] in 'Ww@':
                    break
                elif board[row+j][col-j] in 'Bb$' and in_board(row+(j+1),col-(j+1),N) and board[row+(j+1)][col-(j+1)] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row+(j+1)][col-(j+1)] = '@'
                    temp_board[row][col] = '.'
                    temp_board[row+j][col-j] = '.'
                    board_list.append(temp_board)
                    break  
                    
                elif board[row+j][col-j] in 'Bb$' and in_board(row+(j+1),col-(j+1),N) and board[row+(j+1)][col-(j+1)] != '.' :
                    break
                    

        # Considering moves to left diagonal upwards
        for j in range(1,N):
            if in_board(row-j,col-j,N):
                if board[row-j][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col-j] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col-j] in 'Ww@':
                    break

                elif board[row-j][col-j] in 'Bb$' and in_board(row-(j+1),col-(j+1),N) and board[row-(j+1)][col-(j+1)] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row-(j+1)][col-(j+1)] = '@'
                    temp_board[row][col] = '.'
                    temp_board[row-j][col-j] = '.'
                    board_list.append(temp_board)
                    break
                    
                elif board[row-j][col-j] in 'Bb$' and in_board(row-(j+1),col-(j+1),N) and board[row-(j+1)][col-(j+1)] != '.' :
                    break
                    
     # Moves for the black raichu 
    if board[row][col] == '$':
        temp_board = None
     # Considering moves to the left
        for j in range(1,col+1): 
            if in_board(row,col-j,N):
                if board[row][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row][col-j] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                    
                elif board[row][col-j] in 'Bb$':
                    break
                    
                elif board[row][col-j] in 'Ww@' and in_board(row,col-(j+1),N) and board[row][col-(j+1)] == '.':
                    temp_board = deepcopy(board)
                    temp_board[row][col-(j+1)] = '$'
                    temp_board[row][col] = '.'
                    temp_board[row][col-j] = '.'
                    board_list.append(temp_board)
                    break
                    
                elif board[row][col-j] in 'Ww@' and in_board(row,col-(j+1),N) and board[row][col-(j+1)] != '.':
                    break
                    
        # Considering moves to the right
        j=1
        while in_board(row,col+j,N):
            if board[row][col+j]=='.':
                temp_board = deepcopy(board)
                temp_board[row][col+j] = '$'
                temp_board[row][col] = '.'
                board_list.append(temp_board)
            
            elif board[row][col+j] in 'Bb$':
                break

            elif board[row][col+j] in 'Ww@' and in_board(row,col+(j+1),N) and board[row][col+(j+1)] == '.' :
                temp_board = deepcopy(board)
                temp_board[row][col+(j+1)] = '$'
                temp_board[row][col] = '.'
                temp_board[row][col+j] = '.'
                board_list.append(temp_board)
                break
                
            elif board[row][col+j] in 'Ww@' and in_board(row,col+(j+1),N) and board[row][col+(j+1)] != '.':
                break
                
            j+=1

        # Considering moves to forward
        for j in range(1,N):
            if in_board(row-j,col,N):
                if board[row-j][col]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col] in 'Bb$':
                    break
                    
                elif board[row-j][col] in 'Ww@' and in_board(row-(j+1),col,N) and board[row-(j+1)][col] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row-(j+1)][col] = '$'
                    temp_board[row][col] = '.'
                    temp_board[row-j][col] = '.'
                    board_list.append(temp_board)
                    break
                
                elif board[row-j][col] in 'Ww@' and in_board(row-(j+1),col,N) and board[row-(j+1)][col] != '.' :
                    break
                
        # Considering moves to backwards
        for j in range(1,N):
            if in_board(row+j,col,N):
                if board[row+j][col]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                    
                elif board[row+j][col] in 'Bb$':
                    break

                elif board[row+j][col] in 'Ww@' and in_board(row+(j+1),col,N) and board[row+(j+1)][col] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row+(j+1)][col] = '$'
                    temp_board[row][col] = '.'
                    temp_board[row+j][col] = '.'
                    board_list.append(temp_board)
                    break
                    
                elif board[row+j][col] in 'Ww@' and in_board(row+(j+1),col,N) and board[row+(j+1)][col] != '.' :
                    break
                    
     
        # Considering moves to right diagonal downwards
        for j in range(1,N):
            if in_board(row+j,col+j,N):
                if board[row+j][col+j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col+j] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row+j][col+j] in 'Bb$':
                    break
                    
                elif board[row+j][col+j] in 'Ww@' and in_board(row+(j+1),col+(j+1),N) and board[row+(j+1)][col+(j+1)] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row+(j+1)][col+(j+1)] = '$'
                    temp_board[row][col] = '.'
                    temp_board[row+j][col+j] = '.'
                    board_list.append(temp_board)
                    break
                    
                elif board[row+j][col+j] in 'Ww@' and in_board(row+(j+1),col+(j+1),N) and board[row+(j+1)][col+(j+1)] != '.' :
                    break
        
    
                    
        # Considering moves to right diagonal upwards
        for j in range(1,N):
            if in_board(row-j,col+j,N):
                if board[row-j][col+j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col+j] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col+j] in 'Bb$':
                    break

                elif board[row-j][col+j] in 'Ww@' and in_board(row-(j+1),col+(j+1),N) and board[row-(j+1)][col+(j+1)] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row-(j+1)][col+(j+1)] = '$'
                    temp_board[row][col] = '.'
                    temp_board[row-j][col+j] = '.'
                    board_list.append(temp_board)
                    break
                
                elif board[row-j][col+j] in 'Ww@' and in_board(row-(j+1),col+(j+1),N) and board[row-(j+1)][col+(j+1)] != '.' :
                    break

        # Considering moves to left diagonal downwards
        for j in range(1,N):
            if in_board(row+j,col-j,N):
                if board[row+j][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col-j] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row+j][col-j] in 'Bb$':
                    break

                elif board[row+j][col-j] in 'Ww@' and in_board(row+(j+1),col-(j+1),N) and board[row+(j+1)][col-(j+1)] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row+(j+1)][col-(j+1)] = '$'
                    temp_board[row][col] = '.'
                    temp_board[row+j][col-j] = '.'
                    board_list.append(temp_board)
                    break
                
                elif board[row+j][col-j] in 'Ww@' and in_board(row+(j+1),col-(j+1),N) and board[row+(j+1)][col-(j+1)] != '.' :
                    break

        # Considering moves to left diagonal upwards
        for j in range(1,N):
            if in_board(row-j,col-j,N):
                if board[row-j][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col-j] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col-j] in 'Bb$':
                    break
                    
            
                elif board[row-j][col-j] in 'Ww@' and in_board(row-(j+1),col-(j+1),N) and board[row-(j+1)][col-(j+1)] == '.' :
                    temp_board = deepcopy(board)
                    temp_board[row-(j+1)][col-(j+1)] = '$'
                    temp_board[row][col] = '.'
                    temp_board[row-j][col-j] = '.'
                    board_list.append(temp_board)
                    break
                
                elif board[row-j][col-j] in 'Ww@' and in_board(row-(j+1),col-(j+1),N) and board[row-(j+1)][col-(j+1)] != '.' :
                    break
            
    return board_list

def raichu_succ(board,N,row,col):
    '''
    row : row of raichu
    col : col of raichu
    '''
    board_list = []
    
    # Moves for the white raichu 
    if board[row][col] == '@':
        temp_board = None    
     # Considering moves to the left
        for j in range(1,col+1):
            if in_board(row,col-j,N):
                if board[row][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row][col-j] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row][col-j] in 'Ww@':
                    break

                elif board[row][col-j] in 'Bb$':
                    for k in range(col-j-1,-1,-1):
                        if in_board(row,k,N) and board[row][k] == '.' :
                            temp_board = deepcopy(board) 
                            temp_board[row][k] = '@'
                            temp_board[row][col] = '.'
                            temp_board[row][col-j] = '.'
                            board_list.append(temp_board)
                        elif in_board(row,k,N) and board[row][k]!= '.' :  
                            break
                    break
                    
                # Considering moves to the right 
        for j in range(1,N):
            if in_board(row,col+j,N):
                if board[row][col+j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row][col+j] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row][col+j] in 'Ww@':
                    break

                elif board[row][col+j] in 'Bb$':
                    for k in range(col+j+1,N):
                        if in_board(row,k,N) and board[row][k] == '.' :
                            temp_board = deepcopy(board) 
                            temp_board[row][k] = '@'
                            temp_board[row][col] = '.'
                            temp_board[row][col+j] = '.'
                            board_list.append(temp_board)
                        elif in_board(row,k,N) and board[row][k]!= '.' :  
                            break
                    break
                    

        # Considering moves to forward
        for j in range(1,N):
            if in_board(row+j,col,N):
                if board[row+j][col]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row+j][col] in 'Ww@':
                    break
                
                elif board[row+j][col] in 'Bb$':
                    for k in range(row+j+1,N):
                        if in_board(k,col,N) and board[k][col] == '.' :
                            temp_board = deepcopy(board)
                            temp_board[k][col] = '@'
                            temp_board[row][col] = '.'
                            temp_board[row+j][col] = '.'
                            board_list.append(temp_board)
                        elif in_board(k,col,N) and board[k][col]!= '.' : 
                            break
                    break
                    
        # Considering moves to backwards
        for j in range(1,N):
            if in_board(row-j,col,N):
                if board[row-j][col]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col] in 'Ww@':
                    break

                elif board[row-j][col] in 'Bb$':
                    for k in range(row-j-1,-1,-1):
                        if in_board(k,col,N) and board[k][col] == '.' :
                            temp_board = deepcopy(board)
                            temp_board[k][col] = '@'
                            temp_board[row][col] = '.'
                            temp_board[row-j][col] = '.'
                            board_list.append(temp_board)
                        elif in_board(k,col,N) and board[k][col]!= '.' : 
                            break
                    break
                    
                
        # Considering moves to right diagonal downwards
        for j in range(1,N):
            if in_board(row+j,col+j,N):
                if board[row+j][col+j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col+j] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row+j][col+j] in 'Ww@':
                    break

                elif board[row+j][col+j] in 'Bb$':
                    for k in range(1,N):
                        if in_board(row+(j+k),col+(j+k),N) and board[row+(j+k)][col+(j+k)] == '.' :
                            temp_board = deepcopy(board)
                            temp_board[row+(j+k)][col+(j+k)] = '@'
                            temp_board[row][col] = '.'
                            temp_board[row+j][col+j] = '.'
                            board_list.append(temp_board)
                        elif in_board(row+(j+k),col+(j+k),N) and board[row+(j+k)][col+(j+k)] != '.' : 
                            break
                    break


        # Considering moves to right diagonal upwards
        for j in range(1,N):
            if in_board(row-j,col+j,N):
                if board[row-j][col+j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col+j] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col+j] in 'Ww@':
                    break
                    
                elif board[row-j][col+j] in 'Bb$':
                    for k in range(1,N):
                        if in_board(row-(j+k),col+(j+k),N) and board[row-(j+k)][col+(j+k)] == '.':
                            temp_board = deepcopy(board)
                            temp_board[row-(j+k)][col+(j+k)] = '@' 
                            temp_board[row][col] = '.'
                            temp_board[row-j][col+j] = '.'
                            board_list.append(temp_board)
                        elif in_board(row-(j+k),col+(j+k),N) and board[row-(j+k)][col+(j+k)] != '.':
                            break
                    break
                    
        # Considering moves to left diagonal downwards
        for j in range(1,N):
            if in_board(row+j,col-j,N):
                if board[row+j][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col-j] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row+j][col-j] in 'Ww@':
                    break
                
                elif board[row+j][col-j] in 'Bb$':
                    for k in range(1,N):
                        if in_board(row+(j+k),col-(j+k),N) and board[row+(j+k)][col-(j+k)] == '.' :
                            temp_board = deepcopy(board)
                            temp_board[row+(j+k)][col-(j+k)] = '@'
                            temp_board[row][col] = '.'
                            temp_board[row+j][col-j] = '.'
                            board_list.append(temp_board)
                        elif in_board(row+(j+k),col-(j+k),N) and board[row+(j+k)][col-(j+k)] != '.' :
                            break
                    break
                    

        # Considering moves to left diagonal upwards
        for j in range(1,N):
            if in_board(row-j,col-j,N):
                if board[row-j][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col-j] = '@'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col-j] in 'Ww@':
                    break

                elif board[row-j][col-j] in 'Bb$':
                    for k in range(1,N):
                        if in_board(row-(j+k),col-(j+k),N) and board[row-(j+k)][col-(j+k)] == '.' :
                            temp_board = deepcopy(board)
                            temp_board[row-(j+k)][col-(j+k)] = '@'
                            temp_board[row][col] = '.'
                            temp_board[row-j][col-j] = '.'
                            board_list.append(temp_board)
                        elif in_board(row-(j+k),col-(j+k),N) and board[row-(j+k)][col-(j+k)] != '.' :
                            break
                    break
                    
    
    # Moves for the black raichu 
    if board[row][col] == '$':
        temp_board = None
     # Considering moves to the left
        for j in range(1,col+1): 
            if in_board(row,col-j,N):
                if board[row][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row][col-j] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                    
                elif board[row][col-j] in 'Bb$':
                    break
                    
                elif board[row][col-j] in 'Ww@':
                    for k in range(col-j-1,-1,-1):
                        if in_board(row,k,N) and board[row][k] == '.' :
                            temp_board = deepcopy(board)
                            temp_board[row][k] = '$'
                            temp_board[row][col] = '.'
                            temp_board[row][col-j] = '.'
                            board_list.append(temp_board)
                        elif in_board(row,k,N) and board[row][k]!= '.' : 
                            break
                    break
        
        # Considering moves to the right           
        for j in range(1,N):
            if in_board(row,col+j,N):
                if board[row][col+j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row][col+j] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row][col+j] in 'Bb$':
                    break

                elif board[row][col+j] in 'wW@':
                    for k in range(col+j+1,N):
                        if in_board(row,k,N) and board[row][k] == '.' :
                            temp_board = deepcopy(board) 
                            temp_board[row][k] = '$'
                            temp_board[row][col] = '.'
                            temp_board[row][col+j] = '.'
                            board_list.append(temp_board)
                        elif in_board(row,k,N) and board[row][k]!= '.' :  
                            break
                    break
   
        # Considering moves to forward
        for j in range(1,N):
            if in_board(row-j,col,N):
                if board[row-j][col]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col] in 'Bb$':
                    break
                    
                elif board[row-j][col] in 'Ww@':
                    for k in range(row-j-1,-1,-1):
                        if in_board(k,col,N) and board[k][col] == '.' :
                            temp_board = deepcopy(board)
                            temp_board[k][col] = '$'
                            temp_board[row][col] = '.'
                            temp_board[row-j][col] = '.'
                            board_list.append(temp_board)
                        elif in_board(row,k,N) and board[row][k]!= '.' : 
                            break
                    break

                
        # Considering moves to backwards
        for j in range(1,N):
            if in_board(row+j,col,N):
                if board[row+j][col]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                    
                elif board[row+j][col] in 'Bb$':
                    break

                elif board[row+j][col] in 'Ww@':
                    for k in range(row+j+1,N):
                        if in_board(k,col,N) and board[k][col] == '.':
                            temp_board = deepcopy(board)
                            temp_board[k][col] = '$'
                            temp_board[row][col] = '.'
                            temp_board[row+j][col] = '.'
                            board_list.append(temp_board)
                        elif in_board(k,col,N) and board[k][col]!= '.' : 
                            break
                    break
     
        # Considering moves to right diagonal downwards
        for j in range(1,N):
            if in_board(row+j,col+j,N):
                if board[row+j][col+j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col+j] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row+j][col+j] in 'Bb$':
                    break
                    
                elif board[row+j][col+j] in 'Ww@':
                    for k in range(1,N):
                        if in_board(row+(j+k),col+(j+k),N) and board[row+(j+k)][col+(j+k)] == '.' :
                            temp_board = deepcopy(board)
                            temp_board[row+(j+k)][col+(j+k)] = '$'
                            temp_board[row][col] = '.'
                            temp_board[row+j][col+j] = '.'
                            board_list.append(temp_board)
                        elif board[row+j][col+j] in 'Ww@' and in_board(row+(j+k),col+(j+k),N) and board[row+(j+k)][col+(j+k)] != '.' :
                            break
                    break
        
    
                    
        # Considering moves to right diagonal upwards
        for j in range(1,N):
            if in_board(row-j,col+j,N):
                if board[row-j][col+j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col+j] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col+j] in 'Bb$':
                    break

                elif board[row-j][col+j] in 'Ww@':
                    for k in range(1,N):
                        if in_board(row-(j+k),col+(j+k),N) and board[row-(j+k)][col+(j+k)] == '.' :
                            temp_board = deepcopy(board)
                            temp_board[row-(j+k)][col+(j+k)] = '$'
                            temp_board[row][col] = '.'
                            temp_board[row-j][col+j] = '.'
                            board_list.append(temp_board)
                        elif board[row-j][col+j] in 'Ww@' and in_board(row-(j+k),col+(j+k),N) and board[row-(j+k)][col+(j+k)] != '.' :
                            break
                    break
                    
        # Considering moves to left diagonal downwards
        for j in range(1,N):
            if in_board(row+j,col-j,N):
                if board[row+j][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row+j][col-j] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row+j][col-j] in 'Bb$':
                    break

                elif board[row+j][col-j] in 'Ww@':
                    for k in range(1, N):
                        if in_board(row+(j+k),col-(j+k),N) and board[row+(j+k)][col-(j+k)] == '.' :
                            temp_board = deepcopy(board)
                            temp_board[row+(j+k)][col-(j+k)] = '$'
                            temp_board[row][col] = '.'
                            temp_board[row+j][col-j] = '.'
                            board_list.append(temp_board)
                        elif board[row+j][col-j] in 'Ww@' and in_board(row+(j+k),col-(j+k),N) and board[row+(j+k)][col-(j+k)] != '.' :
                            break
                    break

        # Considering moves to left diagonal upwards
        for j in range(1,N):
            if in_board(row-j,col-j,N):
                if board[row-j][col-j]=='.':
                    temp_board = deepcopy(board)
                    temp_board[row-j][col-j] = '$'
                    temp_board[row][col] = '.'
                    board_list.append(temp_board)
                
                elif board[row-j][col-j] in 'Bb$':
                    break
                    
                elif board[row-j][col-j] in 'Ww@': 
                    for k in range(1,N):
                        if in_board(row-(j+k),col-(j+k),N) and board[row-(j+k)][col-(j+k)] == '.' :
                            temp_board = deepcopy(board)
                            temp_board[row-(j+k)][col-(j+k)] = '$'
                            temp_board[row][col] = '.'
                            temp_board[row-j][col-j] = '.'
                            board_list.append(temp_board)
                        elif board[row-j][col-j] in 'Ww@' and in_board(row-(j+k),col-(j+k),N) and board[row-(j+k)][col-(j+k)] != '.' :
                            break
                    break
            
    return board_list


def generate_successors(board,N,row,col):
    element = board[row][col]
    if element in 'wb':
        return pichu_succ(board,N,row,col)
    elif element in 'WB':
        return pikachu_succ(board,N,row,col)
    elif element in '@$':
        return raichu_succ(board,N,row,col)

def minimax(board,N,depth,player):
    # Approach inspired by this youtube video : 'https://www.youtube.com/watch?v=l-hh51ncgDI&t=494s'

    if depth == 0 or gameover(board,N):
        return (board_score(board,N),board)
    
    if player == 'w': # Maximizing player
        # print("In maximizing")
        maxEval = -9999999999
        final_board = None
        for i in range(N):
            for j in range(N):
                if board[i][j] in 'wW@' :
                    for successor in generate_successors(board,N,i,j):
                        # print(depth)
                        # print_brd(successor)
                        # print()
                        eval,temp_board = minimax(successor,N,depth-1,'b')
                        if eval > maxEval:
                            final_board,maxEval = successor,eval
        return maxEval,final_board

    if player == 'b': # Minimizing player
        # print("In minimizing")
        minEval = 9999999999
        final_board = None
        for i in range(N):
            for j in range(N):
                if board[i][j] in 'bB$' :
                    for successor in generate_successors(board,N,i,j):
                        # print(depth)
                        # print_brd(successor)
                        # print()
                        eval,temp_board = minimax(successor,N,depth-1,'w')
                        if eval < minEval:
                            final_board,minEval = successor,eval
        return minEval,final_board
    
def minimax_1(board,N,depth,alpha,beta,player):
    # Approach inspired by this youtube video : 'https://www.youtube.com/watch?v=l-hh51ncgDI&t=494s'

    if depth == 0 or gameover(board,N):
        return (board_score(board,N),board)
    
    if player == 'w': # Maximizing player
        # print("In maximizing")
        maxEval = -9999999999
        final_board = None
        for i in range(N):
            for j in range(N):
                if board[i][j] in 'wW@' :
                    for successor in generate_successors(board,N,i,j):
                        # print(depth)
                        # print_brd(successor)
                        # print()
                        eval,temp_board = minimax_1(successor,N,depth-1,alpha,beta,'b')
                        if eval > maxEval:
                            final_board,maxEval = successor,eval
                        alpha = max(alpha,eval)
                        if beta<= alpha:
                            break
        return maxEval,final_board

    if player == 'b': # Minimizing player
        # print("In minimizing")
        minEval = 9999999999
        final_board = None
        for i in range(N):
            for j in range(N):
                if board[i][j] in 'bB$' :
                    for successor in generate_successors(board,N,i,j):
                        # print(depth)
                        # print_brd(successor)
                        # print()
                        eval,temp_board = minimax_1(successor,N,depth-1,alpha,beta,'w')
                        if eval < minEval:
                            final_board,minEval = successor,eval
                        beta = min(beta,eval)
                        if beta <= alpha:
                            break
        return minEval,final_board

def gameover(board,N):
    dict_ = {}
    for i in range(N):
        for j in range(N):
            if board[i][j] != '.':
                dict_[board[i][j]] = 1
    str_dict = "".join(sorted(list(dict_.keys())))
#     print(str_dict)
    b_winner_str = 'bB$'
    b_winner_str = "".join(sorted(b_winner_str))
#     print(b_winner_str)
    w_winner_str = 'wW@'
    w_winner_str = "".join(sorted(w_winner_str))  
#     print(w_winner_str)
    if b_winner_str == str_dict or w_winner_str == str_dict:
        return True
    else:
        return False

def print_brd(d):
    for x in d:
        for y in x:
            print(y,end=' ')
        print('')

def find_best_move(board, N, player, timelimit):

    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    # #
    depth = 1
    while True:

        val,board_temp = minimax_1(board_two_dimensional(list(board),N),N,depth,-999999999,99999999,player)
        depth+=1 
        print(depth)
        yield board_temp


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print("".join(flatten_board(new_board)))
