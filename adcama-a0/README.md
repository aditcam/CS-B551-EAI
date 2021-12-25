# a0
## <ins>__Route_Pichu ( Q1 )__

* ## __Problem Abstraction__ :
    * __Valid States__ : The set of all possible states on the map that the pichu can or cannot visit consisting of '.' for visitable locations and 'X' for walls/obstacles and '@' for goal state.
    * __Initial State__ : The start location of Agent (pichu) given by the 'pichu_loc' variable, the agent is represented by 'p'.
    * __Goal State__ : The loation where _'you'_ are located, represented by __'@'__.
    * __Succesor Function__ : The __'moves'__ function is the successor function with returns a list of possible next steps the agent can take to reach its goal state.
    * __Cost Function__ : The cost function is __'1'__ for each move made.  

    <br />

* ## __Solution overview + problems faced + design decisions__ : 

    Here is the approach I used to solve the given problem - 

    * The first thing I found that the code was in an infinite loop, this was mainly because the skeleton code didn't take into account visited nodes and kept looping back to visited nodes thus resulting in a never ending loop. To fix this, I replaced the __' . '__ in visited locations with a __' V '__. Due to this, the successor function wouldn't loop back as it ensures that it can only go to states having __' . '__ or __' @ '__ as characters. _This way of storing visited states meant that I incurred no overhead in terms of space as I leveraged the existing data structure._
    
    * Furthermore the Data structure being used was effectively a **stack** as we were initially popping out elements from the end of the list (Fringe) and appending to the end. To fix this, I used *pop(0)* to essentially remove elements from the beginning and append it to the end thus converting it to a **queue**.
    Why this change of data structure is important is because the search technique I am using is BFS, the reason for choosing BFS is that **complete** and **optimal** ( as the given program has unifrom cost function for each move ). The reason I chose BFS is that this search technique also makes it easier to track the number of moves as it explores paths of the same length across various states thus making the program very systematic. 

    * The main hurdle I faced was printing the path. The approach I came up with was to use a dictionary wherein I stored the current node being explored as the key and the value as the corresponding previous node. On reaching the goal state I then used this dictionary to retrace my path from the goal state to the start state, created a path string corresponding to each move. 

    * _Some intuition for the above paragraph : Initially I felt that the above technique would not yield the correct answer because my dictionary might store incorrect previous nodes from suboptimal paths, but on further analysis it became clear that my program would stop once the goal state is reached, at which point the path leading up to the goal states would be the most recent entries to the dictionary, these recent entries would replace previous suboptimal entries thus allowing us to trace back the correct path._  
    
    <br />
* ## __Q&A__ :
    Q : Why does the program often fail to find a solution? 

    A : the code was in an infinite loop, this was mainly because the skeleton code didn't take into account visited nodes and kept looping back to visited nodes thus resulting in a never ending loop.

    <br />
    <br />

    ## <ins> __Arrange_Pichus ( Q2 )__

* ## __Problem Abstraction__ :
    * __Valid States__ : The set of all possible states on the map having >=1 agent 'p' with obstacles/wall 'X' and visitable states '.' and _'you'_ represented by '@'.  
    * __Initial State__ : A state on the map having obstacles 'X', visitable locations '.' , _'you'_ '@' and one agent 'p'.
    * __Goal State__ : A map state having 'n' (input) pichus in a manner that the 'n' agents cannot view each other and are blocked by either _'you'_ (@) or obstacles/walls' X'.
    * __Succesor Function__ : The __'successors'__ function is the successor function which adds agents to safe locations on the map in order to explore the search tree and find a suitable solution with 'n' (input) number of pichus.
     * __Cost Function__ : The cost function is __'1'__ for each time we place an agent as our functions compute the possible locations to palce the agent.


    <br />

* ## __Solution overview + problems faced + design decisions__ : 

    Here is the approach I used to solve the given problem - 

    * The given skeleton code returns agents (pichus) in consecutive (visible) locations on the map as the final answer so long as they satisfy the condition of 'n' (input), which is not the desired output. To combat this issue I created added another function that, in addition to the existing functionality of successor function in the skeleton code, implements a vital check that makes it possible to get desirable states where the agents cannot see each other. In addition to this, I have used BFS as my search algorithm of choice as it is optimal and complete.

    * The function that I added is called the **'safe_to_place()'** function, this function accepts a house map, row index, column index and the outputs a boolean value depending on whether the agent can be placed at the given location or not.

    * The safe_to_place() calls 3 functions that check whether the agent is safe horizontally, vertically and diagonally, the functions are horizontal_check(), vertical_check(), diagonal_check() which all return booleans, the safe_to_place() essentially returns the logical 'AND' of the 3 aforementioned functions to give the final output.  

    * In each of the above 3 'x'_check functions, what we do is start from the location (row,col) and we check if either sides of horizontal/vertical/diagonal areas ( above & below / right & left / diagonal & anti diagonal ) are safe by checking for other agents 'p'. If we encounter a 'p' at any sub segment of the diagonal/horizontal/vertical we return a false knowing that it is not safe, however if we encounter a 'X', we know it is safe for that diagonal/horizontal/vertical sub-segment. 

    * One minor optimization I have made is that if one sub-segment is False, then return a False instead of checking the other sub-segment. For eg. If we know that the above vertical half of the selected position (row,col) is not safe then we do not need to bother checking the vertical half that is below our point (row,col) 
