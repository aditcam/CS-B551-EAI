# a2

#### Team: Aditya Shekhar Camarushy(adcama@iu.edu), Sai Prajwal Reddy(reddysai@iu.edu), Melissa Rochelle Mathias(melmath@iu.edu)

## **Question 1:**

Raichu: This question deals with generating the next best move to make on a board against an opponent, playing in alternate turns. The pieces can be either black or white (with white starting first) and each color corresponding to a player. There are 3 distinct types of pieces, namely Pichu, Pikachu and Raichu each with their own unique set of moves. 

### **Initial State:**
- The initial state will be a N x N board (N≥8 and N is even) with the 2nd row consisting of white Pikachus and 3rd row consisting white Pichus. On the N-1 and N-2 rows we observe Black Pikachus and Black Pichus respectively. (Pichus and Pikachus are placed in alternate columns in the given rows).

### **Valid states:**
- All the possible states on the board with any arrangements of Pichu, Pikachus and Raichus are considered valid states. (Provided they follow the game rules of the board)

### **Successor Function:** 
- For a given player (white/black) it is the resulting states obtained by making a single valid move following the game's rules for any of the pieces (Pichu, Pikachus or Raichus ) on the board that are of the player's designated color.   

### **Goal State:**
- The board having tiles belonging to only one color (white or black) or a state in which the game is deemed a draw (Due to timeout / as decided by the driver program). 

### Cost/Static Evaluation Function
- While there is no cost function associated with making a move we do have an evaluation function of successor board states that outputs a number (more -ve is better for min player while more +ve is better for max player) which allows us to choose the best state for a given player in a level of the minimax tree. Our evaluation function (called board_score) considered 2 components when scoring a given state - 

    1. The difference between pieces of a specific type amongst the given suits (black and white). Our function to evaluate the board state was as follows - 

        8 * (Number of White Raichus - Black Raichus) + 3 * (Number of White Pikachus - Number of Black Pikachus ) + 2 * (Number of White Pichus - Number of Black Pichus)
        
        **NOTE** : The reasoning behind choosing 2,3 and 8 as weights was because they correspond to the number of directions each piece can make.  
    
    2. The next factor we used to score a states was to check the immediate surroundings of each given piece and inidvidually score them accordingly, based on how susceptible they may be to an attack. Pieces adjacent to pieces of their own kind were scored higher as they were less susceptible to attack from atleast 2 directions (for a single adjacent piece) and pieces at the edge of the board/ at corners of the board also score higher (But we give higher importance to pieces that are adjacent to their own kind). 
    
        We also reduce the score when pieces of the opposite suit are adjacent although we give this less importance than having a piece of the same suit as the piece with the same suit will definitely reduce our susceptibility to attack but the piece from the opposite suite may or may not be able to attack us.  

### Code Provided: 
- The skeleton code was returning a hardcoded static result yielding the same board as the original question. 

### Approach: 

- The approach we used to solve this question was to use Alpha-Beta Pruning on top of the minmax algorithm (adversarial search). The steps involved in finding the next best move are as follows - 
The below psudeo code was taken from the youtube video : https://www.youtube.com/watch?v=l-hh51ncgDI, this is what we referred to to build our algorithm for alpha beta pruninig.

        function minimax(position, depth, alpha, beta, maximizingPlayer)
            if depth == 0 or game over in position
                return static evaluation of position
        
            if maximizingPlayer
                maxEval = -infinity
                for each child of position
                    eval = minimax(child, depth - 1, alpha, beta false)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha
                        break
                return maxEval
        
            else
                minEval = +infinity
                for each child of position
                    eval = minimax(child, depth - 1, alpha, beta true)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha
                        break
                return minEval


- We created a function to generate successor states (1 move away) for each piece on the board following the below rules -   
        
    -  Pichu's: 
    
        - It can move only diagonally forward if the square is empty.
    
        - It can and can only jump over/attack pichu's of the opposite player/color, by moving two squares diagonally forward, if the square is empty. The jumped piece is removed from the board as soon as it was jumped.
    
    - Pikachu:
    
        - It can move 1 or 2 steps either forward, left or right to an empty space, but it does have to keep in mind that the squares between them are also empty.
    
        - They cannot move diagonally.
    
        - They can jump over pichu's and pikachu's of the opposite player/color, by moving 2-3 steps forward, left or right, but not in diagonally, again keeping in mind that the pieces between the pikachu's position and the jumped piece are empty and the position after the jumped piece is also empty.
    
        - The jumped piece should be removed as soon as it is jumped.
    
     - Raichu:
     
        - Raichu is craeted when it a pichu or pikachu reaches the opposite side of the the board.
    
        - Raichu can move in any number of squares and in all directions i.e forward, backwards, left , right and diagonally.

        -  Raichu can jump over a single pichu, Pikachu or Raichu of the opposite player/color, and landing any number of steps farther , as long as the squares between the jumped piece and Raichu are empty.

        - The jumped piece is removed as soon as it is jumped over.

- Lastly we executed the minimax in a depthwise fashion starting from the depth of 1, the idea with this was to continuosly yield the best solution at a given point of time so as to meet the time threshold to generate the next best move. Basically, with increasing depth, the algorithm has more information based on which it can make a better decision, but the disadvantage with increasing the depth is that the number of successors can become too large and make computation painfully slow, therefore it helps to get answers in a depthwise fashion. 

 ### **Challenges encountered**
-  #### Challenge 1: 
    - We had to generate a huge number of successors as the states were comparatively more to a tic tac toe game, i.e the branching factor here was much more than that of a tic-tac-toe game and therefore the code was massive.

- #### Challenge 2:
    - The number of successor states generated for a state as so many in number at some times that we wouldn't get to stage where we get to choose that best state and may end up choosing a sub-optimal move as our successor state.
    
- #### Challenge 3: 
    - The scoring function /heuristic that we used here was giving a particular piece a fixed value,for e.g the white pichu,pikachu and raichu were given +2,+3 and +8 values and similarly black pichu, pikachu and raichu was given -2,-3, and -8. We added various conditions based on how susceptible a piece may be to getting attacked and also thought of incentivsing pieces to move ahead as it may maximize the chance of getting a raichu, but what we noticed was keeping the pieces closer together rather than opening up the board actually increased our chance of winning, besides we felt that going forward was not the best move in every scenario. 

## **Question 2:**

### **Quintris:**

 In this question, there are random pieces consisting of 5 blocks arranged in different shapes, which from the top of the board to the bottom. As the piece keeps falling the player can change the shape of the piece by rotating , flipping it horizontally, and move it from left to right. The piece stops when it hits the ground or on another fallen piece. If the piece completes an entire row, the row disappears and the player gets a point.

### **Initial State:**
The initial state will be an empty board with 25 rows and 15 columns. 

### **Valid states:**
- All the possible states on the board with any arrangements of pieces that obey the rules/bounds of the board. 

### **Successor Function:**
Here there are 3 successor functions
The left successor will move the piece one step to the left and then drops it to the ground, this board is then saved as one of the possible successors. Similarly, we get the different boards with placements of the piece in different columns to the left from the initial position it was in.
The right successor will also do the same thing, that is returning the boards with placements of the piece towards the right from its initial position.
The rotation successor, will recursively rotate the piece once at 90 degrees and then generate more successors using the left and right successor. Hence, we would have multiple boards which have the piece in all possible valid positions of the board.

### **Evaluation Function:**
For the Evaluation function that can be placed, we first weighted the rows and columns of the board. The weights are placed in such a way that the lowest row gets the lowest weight and the highest row gets the highest weight. This is done similarly to the columns too, where in the left most column gets the lowest weight and the rightmost column gets the highest weight. We then multiply each row weight or column weight with the number of the x’s in the particular row and column. We then get the minimum value for the row and column and use that position to place the piece in.

### **Goal State:**
The board gets filled up and the player's score is returned. 


## **Question3**

Truth be Told: In this question, we are given a dataset of user-generated reviews in the form of training dataset and testing dataset. 
We are supposed to create a 'Naive Bayes classifier', which classifies the reviews into fake or legitimate for 20 hotels in Chicago. 
The training dataset has labels which tell if the review is 'deceptive'  or 'truthful' along with the review. 

### **Bayesian Classifier:**
To classify the reviews into 'deceptive' and 'truthful', we tried to calculate the probability that a given review is 'truthful' conditioned that it has the words('*P('truthful'|words)'*). Otherwise, it is 'deceptive'. 

* We first get the training data file('deceptive.train.txt') into the form of a dictionary called train_data which has the keys 'labels','objects' and 'classes'. The values for each of the keys is in the form of lists. The values for 'labels' is whether the particular review is 'truthful' or 'deceptive'. In the case of the value for 'objects', it is a list of all the reviews. And finally the value for 'classes' is a list of possible cases i.e 'truthful' or 'deceptive'.

* We then use a python library package called 're' for regular expressions. We use regular expressions to remove all the punctuation marks in the reviews in both training and testing data.

* After we remove the punctuation marks from the reviews, we strip the sentences of any whitespaces at the front and back of the sentence and then, lowercase all the characters in the review. 

* We then store all the words in a dictionary called all_words with the word as the key and the value as a tuple of two numbers in which the first is the number of times a word repeats when the review is 'truthful' and the second being when the same word repeats when the review is 'deceptive'.

* We then use the dictionary of all_words to calculate the probabilities of the unique words, both in the case of 'truthful' and 'deceptive'. We are calculating the probability of the given word, conditioned that the review is 'truthful' or 'deceptive'.(*(P(word|'truthful') or P(word|'deceptive')*)

* We also calculate the probability of the given message being 'truthful' or 'deceptive' by counting the number of occurences of the word 'truthful' and 'deceptive' and dividing it by the length of train_data['labels'].

* We then run a for loop for all the words of each of the review in the test data set. We get the probability that is already calculated for each word and multiply it to the corresponding truthful probability or deceptive probability.(*(P('truthful') * P(word1|truthful) * P(word2|truthful)...)  and (P('deceptive') * P(word1|deceptive) P(word2|deceptive)...)*)

* We store each of the above calculated probability into variables called prob_t and prob_d. We then divide the prob_t by prob_d for each review and if the value is greater than 1, then we store the result as 'truthful' otherwise it is 'deceptive'.

### **Result:**
The Result is stored in the form of a list which contains if the given review in each of the test data set is 'truthful' or 'deceptive'. 
We are getting a accuracy of 79%.
