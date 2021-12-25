
#### Team: Aditya Shekhar Camarushy(adcama@iu.edu), Sai Prajwal Reddy(reddysai@iu.edu), Melissa Rochelle Mathias(melmath@iu.edu)

## **Question 1:**

The 2021 Puzzle: This question expects us to sort a 5*5 puzzle without any empty slot which is initially in the misplaced state. The moves that we can do here are:
- sliding an entire row of tiles left or right one space, with the left- or right-most tile ‘wrapping around’ to the other side of the board, 
- sliding an entire column of tiles up or down one space, with the top- or bottom-most tile ‘wrapping around’ to the other side of the board, 
- rotating the outer ‘ring’ of tiles either clockwise or counterclockwise, or 
- rotating the inner ring either clockwise or counterclockwise 

### **Initial State:**
- The initial state will be a 5*5 board with be randomly misplaced tiles numbered from 1-25. 

### **Valid states:**
- All the possible moves are considered as valid moves. i.e  we can slide the rows to the right or the left / we can slide columns up or down / even have inner and outer rotations both in counter-clockwise and clockwise direction.

### **Successor Function:** 
- All the resulting states obtained by making each kind of move i.e. One row that can be moved either to right and left, one column that can be moved either up and down, or there could be in the inner ring or outer ring rotations which can be moved counterclockwise or clockwise. Our successor function generates 24 states (10 for row shifts + 10 for column shifts + 2 for inner rotations + 2 for outer rotations)

### **Goal State:**
- The board with the tiles in numerically sorted state from 1-25.

### Cost Function:
- The cost of shifting a row, column or an entire inner / outer ring counter-clockwise or clockwise is counted as 1.

#### Code Provided: 
- The skeleton code was returning a hardcoded static result in the form of steps to the solve the board0.

### Approach: 

- In attempt to make the code *modular*, *readable* and more *convenient* to use we have modeled each state as an object belonging to the class **'State'** ( following the principles of **Object oriented programming** ) having attributes relevant to states such as the path to the state, board, move made to reach current board, f(n), g(n), h(n) .etc.

- We have also overriden the \__eq()__ class method in order to make comparision of object classes easier. In fact this is where we handle the case of discard duplicate states that are already present in visited list or priority queue but have a worse f value.

 - The approach we used was a A* algorithm and used number of misplaced tiles as the heuristic function. In the successor function , we  call all the row successors, column succesors, and the inner and outer ring clockwise and counterclockwise successors , we append all the successors we receive into a priority queue (Ordered by the *'f'* score) and then compute the heuristic values for all of them and select the best successor with the least f(n) score. (This is handled by the inherent ordering of a priority queue : We used a list and sorted it based on f as we built a custom class to store states)

- Whenever we get a successor that is the best move according to our heuristic (present at the top of the priority queue) we go to that move for exploration and this repeats until we reach a goal state.  

- When appending our new successors to the priority queue, we always ensure that if this successor is already in the priority queue (same board state), we only append if the current f is lower than the f of the existing same state in the priority queue. 

- There is also a visited list, which consists of visited states, if the f of those successors which have the same board state is lower than the f of the current successor then we skip this successor, else we append it.  

- This process is repeated until we reach the goal state.

**Answer 1.1 :** 

- *In this problem, branching factor of the search tree is 24, that is 10 successors from the row sliding (5 right, 5 left), 10 combination from the column sliding(5 up and 5 down) and 4 combinations from the inner and outer ring rotations(Icc, Ic, Occ and Oc), considering the clockwise and counter clockwise rotations.*

 **Answer 1.2 :** 
 -  *If the solution can be reached in 7 moves, then in absolute the worst case for BFS, we will have to explore **1 + 24 + 24^2 + 24^3 + 24^4 + 24^5 + 24^6 + 24^7** and for the absolute best case scenario we will have to explore **1 + 24 + 24^2 + 24^3 + 24^4 + 24^5 + 24^6 + 1** states.* 
 
 
 -  **Based on these observations, we can say that a rough answer for the number of states explored for a BFS search would be in the order of 24^7.**

 ### **Challeneges encountered**
-  #### Challenge 1: 
    - The main challenge we faced  (unfortunately also our reason for late submission) was the high run time of our program (Which was initially ~50s for board0.5, currently ~2.8s). Despite manually checking the algorithm for extra states being visited, unnecessary iterations we found nothing while debugging. 

    - We then used the time module to find out which segment of the code caused the delay. It turns out that checking the visited list took about 95% of the total time taken to execute. This was because we used a list to check the visited list. On converting it to a hash dicitionary we were able to check the visited states much quicker and this solved our predicament. 
- #### Challenge 2:
    - Comparing class objects was something new and we had to learn about overriding the special dunder class methods such as \__eq()__ and \__lt()__ .etc. 

- #### Challenge 3: 
    - While solving challenge 1 we had to use hashing, another problem we faced was that the board was a 2d list (converted by us as it was convenient to work with, easy to modify due to list's mutability).

    - The issue we faced was that mutable types such as 2d lists can't be hashed we had to convert them to tuples and explicitly call the hash function on them. 

    - https://eng.lyft.com/hashing-and-equality-in-python-2ea8c738fb9d

- #### Challenge 4: 
    - Creating an admissible heuristic. While we managed to devise an admissible heuristic, it performed rather poorly for some reason (in terms of time and states being visited). Due to this we stuck to the inadmissible heuristic of misplaced tiles as it gave us a much quicker output.

    - We generated a cost matrix for every element depending on the minimum number of moves it required to get from the wrong state to the correct state (We observed a pattern to shift rows/ columns and get the cost matrix for each state). for eg below is the cost matrix for 1 -

        __________________
        1
        __________________
        0 	1 	2 	2 	1 	

        1 	2 	3 	3 	2 	

        2 	3 	4 	4 	3 	

        2 	3 	4 	4 	3 	
        
        1 	2 	3 	3 	2 	

        eg. If 1 is in position (0,1) it takes one move to get 1 in the right position. 
        eg. If 1 is in the position (1,3) it will take 3 moves to get 1 in the right place.

    - This was then computed for each element and the total number of moves were divided by 16. Thus reuslting in a max value of 4 moves in the worst case, we were unable to disprove admissibility in any case. (Code is also present and commented however)


## **Question 2:** 

Road trip: In this question we have been given a dataset of major highway segments of the United States, which includes highway names, distances, and speed limits on the respective paths. Along with this we have also receive a dataset of cities and towns with corresponding latitude-longitude positions. 

We need to find driving directions between the start city and end city entered by the user while optimizing for distance/ time/ delivery-time/ segments traversed. We also have to return the *"total-segments", "total-miles", "total-hours", "total-delivery-hours", "route-taken"* while optimizing for each paramter. 

The user also selects the cost function they want to optimize for. ie. *distance, time, segments, delivery.*

### **Initial State:** 
- The start city that is given as input from which we need to find the best route to the destination city. This start city will be considered as our initial state.

### **Valid states**
- All the existing paths between two given cities are considered as valid states.

### **Successor Function:**
- Returns all the cities that can be reached from the current city. (We also ensure that a previous visited city is not generated as a part of the successors, but this is only when we generate successors. *It is possible to come across the same state multiple times with a different possible f score*)

### **Goal State:**
- The destination state i.e The end city given by the user. We provide giving the optimal results based on the cost function that we gave input, i.e we need to display the best route, with the best distance/ number of segments/ time to reach the destination/ the delivery time taken between the 2 cities.

### **Cost Function and Heuristic explanation:**

 The Cost Function(g) is the numerical value from the start state to the current state. The Heuristic cost(h) is the estimated numerical value from the current state to the goal state.

- Distance:
    - Cost(g): The cost function is the distance from the start city to the current city in the route. It is calculated from the 'road-segments.txt' file which has the details of the highways from various cities along with the distance in miles.
    - Heuristic(h): The heuristic is the estimated distance from the current city in the route to the end city. The estimated distance from a particular city is calculated as an 'euclidean distance' using latitiude and longitude. Wherever the latitude and longitude details where unavailable, we calculated the heuristic by subracting the cost value from the previous heuristic. This gives an approximate distance of the current city or junction from the end city.


- Time:
    - Cost(g): The cost function is the time taken to travel from the start city to the current city. The time taken is calculated as distance divided by speed. Distance and speed are obtained from the 'road-segments.txt' file which had the distance in miles and the speed limit in miles per hour. It was assumed that we are travelling at the uniform max speed limit of the particular highway.
    - Heuristic(h): The heuristic is the estimated time taken to travel from the current city to the end city. The estimated time is calculated again as distance divided by speed. The distance was calculated as 'euclidean distance' using latitude and longitude from the 'city-gps.txt' file which has the city name along with the latitude and longitude. For the cities or junctions for which the latitude and longitude were unavailable, the distance was calculated by calculating the total_distance between the start city and end city, and then subracting from it the distance which had been travelled till the current city. We then took this distance and divided it by the maximum speed limit.


- Segments:
    - Cost(g): The cost function is the number of segments it takes to travel from the start city to the current city. The number of segments is calculated by adding one each time we transverse a route.
    - Heuristic(h) : The heurisitic function is the estimated number of segments it takes to travel from the current city to the end city. We took the heuristic function for segments to always be '1'. We are assuming that the number of segments it takes to reach the end city is 1 from the current city.


- Delivery Time:
    - Cost(g): To minimize the amount of time taken for delivery, we need to make sure that the amount of time taken  is less. Hence, we choose the same calculation as of time.
    - Heuristic(h): We calculate the amount of delivery time it takes by using the distance and speed limit. Here also we assume that the truck travels at uniform maximum speed limit. Hence, we calculate the estimated delivery time by using the formulaes from the question.

### **Assumptions**
- We assumed that the vehicle travels at uniform maximum speed limit for that particular highway.
- We also assumed that all the highways allow the vehicles to travel in both the directions and none of them are one ways as mentioned in the question.

### **Code provided:**
- The skeleton code was initially returning a static best route between Bloomington,_Indiana Indianapolis,_Indiana , along with total segments taken , total miles , total hours , and total delivery time between the input cities.

### **Approach:** 
- In this code we have again used the A* algorithm yet again (Further explained below). We store the city-gps.txt data  into a dictionary named city_lat_long , which contains the city names (as keys), latuitude and longtiude of the city in form of a tuple (as value).

- We have stored the road-segments.txt into a dictionary named road_segments , containing  one line per road segment connecting two cities.
The space delimited fields are:

    - first city
    - second city
    - distance (in miles)
    - speed limit (in miles per hour)
    - highway name

- From the above point, first city and seconds city stored in a tuple serve as a key, the value is a dictionary consisting of distance, speed limit and highway as keys and their corresponding values as the values of the dictionary.

- In attempt to make the code *modular*, *readable* and more *convenient* to use we have modeled each state as an object belonging to the class **'State'** ( following the principles of **Object oriented programming** ) having attributes relevant to states such as the path to the state, source city, destination city, speed limit for current route from source to destination city, highway name, f(n), g(n) and h (n) .etc. 

- We have also overriden the \__eq()__ class method in order to make comparision of object classes easier. In fact this is where we handle the case of discard duplicate states that are already present in visited list or priority queue but have a worse f value.

 - As mentioned above, the approach we used was a A* algorithm and various heuristic functions for distance, segments, time and delivery time (As explained above). In the successor function, we return all the neighbouring paths that are possible from our current location as State objects. 
 
 - We then append all the successor objects we receive into a priority queue (Ordered by the *'f'* score) and then compute the heuristic values for all of them and select the best successor (pop the successor with least f score out of the priority queue) with the least f(n) score for exploration. (This is handled by the inherent ordering of a priority queue : We used a list and repeatedly sorted it based on f as we built a custom class to store states).

- Whenever we get a successor that is the best move according to our heuristic (present at the top of the priority queue) we go to that move for exploration and this repeats until we reach a goal state.  

- When appending our new successors to the priority queue, we always ensure that if this successor is already in the priority queue (same board state), we only append if the current f is lower than the f of the existing same state in the priority queue. 

- There is also a visited list, which consists of visited states, if the f of those successors which have the same board state is lower than the f of the current successor then we skip this successor, else we append it.  

- This process is repeated until we reach the goal state.

# Question 3:

Choosing teams: The third question is about assigning groups/teams for an assignment based on student preferences in a manner that the time taken by faculty to resolve student conflicts is minimum. Here, each student is sent an electronic survey and asked to fill their preferences.

The questions asked in the survey include the student's desired number of team-members ( they can work individually or teamup in groups of 2-3, where we need to add hyphen separated userids including own email id). If the student does not have teammates in mind while filling the form they can just add 'zzz' (or 'xxx' as per the test case files) for each team member and will get assigned to random people as teammates. Also, the student does not want to work with certain people, they can mention their userids (separated by commas, e.g. userid1,userid2,userid3). 

The total conflict resolution cost ( in terms of time ) depends on various factors like the number of teams, whether person is not assigned to a team that was preferred by him/ her or even the size of the group the student is assigned to.

The objective here is to generate student groups in best accordance with their preferences such that the total conflict resolution cost is the minimum for the faculty members of the course.

### **Initial State:** 
- Randomly generated groups of students having size less than or equal to 3.

### **Valid states:**
- All groups that are randomly generated, ensuring group strength should be at most 3 students and at least 1 one student.  

### **Successor Function:** 
- Returns all valid combination of groups that will be generated by changing the position of just one student (order of students within/across groups is irrelevant) i.e. these successors would be considered as Neighbouring states. The total cost of the generated group. 

### **Goal State:**
- A group that least incurs the least total cost of conflict resolution in terms of time, while also considering the preferences of the students.

### **Cost Function:**
- ![image](https://media.github.iu.edu/user/18433/files/10c34800-2a26-11ec-9ede-ff6f00911778)

		   
### **Code provided:**
- The skeleton code is initially returning a static hardcoded groups along with thier total cost for the groups generated depending on which of their preferences were matched and which weren't.

### **Approach:**    

- The main approach used to solve this problem was to leverage the concept of local search. The reason we used this approach was because the given problem is computationally hard and it is easy to traverse the solution space of candidate solutions by simply changing the position of one given student at a time (local changes) and checking the computed cost (in terms of time) for the new set of groups obtained by shifting a single student until a local minimum (minimum time cost) is obtained. 

- This entire process of obtaining a local minimum is repeated (using an infinite loop) for different randomly generated starts states until we reach a the least possible cost / global minimum (by which point the program's time bound presumably elapses).

- To elaborate on the previous paragraph, we first stored each student's preferences in the form of a dictionary, for example - 

    *'djcran': {'group': ['djcran', 'vkvats', 'nthakurd'], 'avoid': ['sahmaini'], 'req_size': 3}*  

    is one of the entries for a given student with ID : djcran.

- **Step 1** : We use the student IDs to generate random start states using the *random* module present in python. We took random samples of students of sizes 1,2,3 until all the students were assigned to a group and used this random group as the start state. 

- **Step 2** : After generating a random start state we then generated all neighbours/successors which could be obtanined by moving 1 student into a different group (all possible combinations) and from these succerssors we selected the ones having the minimum cost (current local minimum/ best newly generated successor ) and used that as the start state for the next iterations. 

- **Step 3** : If at any point during these iterations, if the local minimum of the best newly generated successor is greater than the existing local minimum from the previously generated states, we then break out of the iteration with our local minimum and yield the answer if it has a lesser cost than our global minimum (and also set the global minimum). If the cost of the local minimum is greater than the global minimum, we simply break out without yielding an answer.  

- **Step 4** : Go back to Step 1.

- This process repeats until we get the best possible output within the existing time bounds.

### **Challenges:**
Initially we noticed that the successors could vary widely depending on the start state and therefore leading to suboptimal solutions most of the times, this prompted us to start with a much more deliberate state where we minimised the cost as much as possible manually, the issue however, was that this led us to just a local minimum which was not necessarily the best. We therefore decided to use random states which would have a much better chance of convergence to a lesser cost (in terms of time).

