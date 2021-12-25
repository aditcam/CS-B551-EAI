# adcama-melmath-reddysai-a3
a3 created for adcama-melmath-reddysai
### Question 1
* Part of Speech Tagging:
In this question, we are supposed to mark every word in a sentence with its part of speech using Bayes Networks. We are supposed to do it using three methods, one being the ‘simplified’ Bayes net method, the second method being ‘hmm_viterbi’, which incorporates a richer Bayes net model and finally, the third method being ‘complex_mcmc’ which also uses Gibbs Sampling to sample posterior distribution along with Bayes Net.
* Training Data:
The training data that we got was in the file called ‘bc.train’. The file consisted of individual sentences in each line, where in each word of the sentence is followed by a part of speech tag. 
* Initial Code:
The skeletal code provided by the professor, returned ‘noun’ as the part of speech tag for every word in the test sentence, for all the three methods. This ended up giving an 18.60% correct tagging for the words and 0% for the sentences for all three approaches.
* Approach:
We have saved the 12 different types of parts of speech tagging in a list called pos_list, we kept a track of the counts of the following factors from the bc.train file, which was used further to calculate emission, initial and transition probabilities:
  *	count_of_number_words  : The total count of the words in the train file. 
  *	 word_count: This dictionary contains the occurrences of the individual words in the train datafile i.e {‘The’:1}
  *	Pos_count: This dictionary contains the count of the pos occurrences e.g. {‘det’:1} 
  *	word_pos_count : This dictionary contains the count of the word having  a certain part of speech tagging , e.g. {‘The|det’:1}
  *	pos_word_count: This dictionary contains the count of the pos being a word ,e.g. {‘det|The’:1}
  *	pos_pos_count : This dictionary has count of the current pos being with the adjacent pos in the list e.g.:{(‘det,noun’:1), (‘det,verb’:1), (‘det,adj’:1)..and so on}
  *	starting_pos_count: This dictionary has the count of a certain pos being at the start of the sentence.
Using the above count dictionaries, we are calculating the probabilities that are required for the part of speech tagging. The different probability dictionaries are:
  *	word_prob :  This dictionary has the probabilities of a particular word occurring in a sentence. i.e. P(‘the’)
  *	pos_prob: This dictionary has the probabilities of a particular pos occurring in a sentence.i.e P(‘det’)
  *	word_pos_prob: This dictionary has the probability of a word given that of a pos. i.e P(‘the’|’det’)
  *	pos_word_prob: This dictionary has the probability of a pos given that of a word. i.e P(‘det’|’the’)
  *	starting_pos_prob: This dictionary has the probability of a certain pos of the word starting at the sentence. 
#### Simplified:
In simplified, we initially create an list called ‘result’, which consists of  ‘noun’ for the entire length of the sentence. We, then run a for loop for the length of the sentence and check the probability of the word given a certain pos, for the all the part of speech tags. For every probability that is greater than the value ‘prob’ which was initially zero, we assign the new maximum probability value to ‘prob’ and change the tag in the result list to the tag which gave maximum  probability.
This method gave us an accuracy of 93.95% for words and 47.50% of the sentences being correctly tagged.
As this is a basic model, it performed average.
#### Hidden Markov Models Viterbi:
In Viterbi, we consider not only emission probability, but also transition probability and initial probability for getting the correct tag for a particular word.
We initially create two empty lists called result and prob and then run a for loop for the entire sentence. We then calculate the emission probability for each pos wherein if the word is present, then we get the count of the number of times the pos is present given that of a certain word. We then check if it’s at the start of a sentence and if it is at the beginning of the sentence, then the probability of it being a certain pos is given by the product of emission probability and probability that a given pos is present at the beginning of a sentence(‘starting_pos_prob’). We store this value in the prob list.
If it’s not at the beginning of the sentence, then we create a temporary dictionary and then calculate the value of the probability which is the product of the probability of the previous word having a certain tag value and the transitional probability. We, then take a max of the values from temp and then multiply the maximum value from temp to the emission probability value and then store it again in the prob list.
We then again get the maximum probability value from the prob list and then check if the probability value in the prob list is equal to it and if its equal to it then we append the corresponding part of speech tag to result.
This method gave us an accuracy of 94.37% for words and 50.75% of the sentences being correctly tagged.
In this approach, the probability also depends on the previous state, and hence it performs better than the simplified Bayesian nets approach, which doesn’t depend on the previous state.
#### Markov Chain Monte Carlo:
In MCMC, we use the Gibbs sampling approach wherein we randomly generate samples. Here the probability depends on the previous state and the current state. 
We get the random value by running it on the simplified function rather than using the random function.
We initially create an empty dictionary called, ‘final_count’. We then run the for loop a certain number of times(in this case we are running it 100 times), along with another for loop for iterating the words in the sentences. We then, initialize an empty list, in which we store every probability value that we calculate. If the sentence has only one word, then we calculate the probability of the word with every pos tag and get the log value of it and then store it in the empty list which was initially create. Or else, if the index is at the beginning of the sentence, then again we calculate the probability of the word given that of a pos and then add it to the probability of a certain pos being at the beginning of the sentence and also add the transitional probability of the pos given that of the random pos. We take log on each of these and then sum them up and store it in the list which was initially created. Else if the index is equal to the length of the random value minus one, then we calculate the emission probability of the word given a certain pos, the transitional probability of the random value of the previous random pos and the current random pos, the emission probability of the word given the previous random pos and finally the transitional probability of the current pos given that of the previous random pos. We again take the log of the values and then append it to initial empty temporary list. If the index does not satisfy any of the above conditions, then probability is calculated by the sum of log of the emission probabilities of the current word given that of pos, emission probability of the previous word given that of the previous random pos , emission probability of the current word given that of the previous random pos, emission probability of the next word given that of the current random pos, emission probability of the next word given that of the next random pos, transitional probability of the previous random pos with all the possible values of  pos given that of the next random pos. We, then add the sum and store in the initial temporary list again.
We, then get a random integer between 1 and 0 and then add all the possible probabilities. We, then check if the sum is greater than the random value which was generated, and in case it is greater then we store the value of the pos tag. We then try getting the pos tag that has the highest probability and store it in a list. This list is the output of the mcmc algorithm that contains the pos tag of the sentences.
This method gave us an accuracy of 94.27% for words and 50.50% of the sentences being correctly tagged.


### Question 3
* Reading Text: 
In this question we need to recognize text in the image, character by character, but images given images are noisy which makes it difficult for the text in the image to be recognized with accuracy.
* Assumptions:
  *	Image has English words and sentences.
  *	 Image has the same fixed-width font of the same size. i.e. each letter is in a box that is 16 pixels wide and 25 pixels tall.
  *	Another assumption we take here is that we consider only 26 uppercase Latin characters, 26 lowercase characters, 10 digits, spaces, 7 punctuations symbols.
* Initial code: The skeletal code provided does the I/O of the image, it converts the image into list of lists that represents a 2 grid of black and white dots.
* Approach:

We use bc.train file from the part 1, but by skipping the even positions which will help us ignore the words  pos tag , to calculate initial, emission and transitional probabilities.
 
For calculating the emission probability, we keep a count of various factors:
  * black_count_test: has the count of the ‘*’ that occurs in the in the test data
  *	black_count_train: has the count of the ‘*’ that occurs in the in the train data
  *	black: has the count of ‘*’ that are matching of the word that we get in the image and what we get in the train data file
  *	white: has the count of ‘ ’ that are matching of the word that we get in the image and what we get in the train data file
  *	no_match_black: has the count of ‘*’ that do not match from the image/test and in train file
  *	no_match_white: has the count of ‘ ’ that do not match from the image and in train file

For calculating the emission probability, we tried different weights for all variables , keeping in mind he density of the pixels, and after much experimentation we settled on the following weights, which gave us a more accurate reading of the text in the image. 

if the probability of getting ‘*’ count  in the test data is more than that of the probability of ‘*’ in train data then we have weights as :
  *	75% for ‘*’ i.e black variable
  *	75%, of white i.e ‘ ’ 
  *	25% for both  no_match_black and no_match_white.

Else the weights will be as follows:
  * 97% for ‘*’ i.e black variable
  *	75% for ‘ ’ i.e white variable
  *	25% for ‘*’ i.e no_match_black variable
  *	3% for no_match_white variable

#### Simplified Bayes Net: 
In this approach, using emission probability, we get the character that has the maximum probability, which we join into the resultant string and give that as output.

#### Hidden Markov Models-Viterbi:

Here we are maintaining 2 lists, with names current_letter and prev_letter which helps us store the emission and transitional probabilities , initialized initially to None with a length of 128 as there are 128 characters in ASCII. This is done so that we can easily map the ASCII value to the character that we get in the image.
So here, we run though the letter in the train and test, for the first character in the test data, we calculate the probability, we take the negative log of the letter, we take negative log here  because to minimize the cost, and then we get the ASCII value (Unicode code value) of the train_letter using the ord function.
 
If the character is not first, we create a temp list, to calculate the transitional probability from the previous letter conditioned on the current letter and append the transitional probability to the temp list.

We then get the character that has the minimum cost value, we add it to the emission probability.
 Then from the list of cost,  we get the minimum cost which represents the maximum probability and print that out as the output.
 
 #### Team: Aditya Shekhar Camarushy(adcama@iu.edu), Sai Prajwal Reddy(reddysai@iu.edu), Melissa Rochelle Mathias(melmath@iu.edu)
<hr>

# a3 
## Part 2 : Ice Tracking 

- The objective of this question is to find the boundaries between air-ice and ice-bedrock given a radar echogram image, there are 3 possible ways of finding the output -   

    1. Using a simplified bayes net model that depends on the intensity (Darkness) of the pixel.

    2. Using the Viterbi algorithm. Which uses the intensity of the pixels and also the fact that the next pixel in the next column of the boundary should be relatively close to the current pixel ( this is to encourage smoothness in our boundary ).

    3. Using the Viterbi algorithm in conjunction with human input ( an actual point on the air-ice or ice-bedrock boundary ) so as to improve the output of the program.

- Since we modeled this as a HMM there we need to compute the Emission, Prior and Transition probabilities -

    1) Emission -
            
        The edge strength array gave us values based on relative intensity of the boundaries, using this we were able to compute probabilities by dividing the each element by the sum of all the edge strength elements in the respective column.

    2) Transition - 

        The idea here was to ensure that the boundary between air-ice/ice-rock is smooth, we incentivize this by setting the transition probabilities from a pixel in a given column to a pixel in the next column such that if the next column index is much larger/ smaller than the current pixel then the transition probability of this happening is very low, if the next column is nearer to the current column, we then give it a higher transition probability as this is conducive to having a smoother boundary. 

        In our scenario, we have considered checking ± 5 columns in the next column by giving them the following probabilities [0 -> 0.25, 1 -> 0.2, 2 -> 0.1, 3-> 0.05, 4 -> 0.0175, 5 -> 0.0075], each of whose _key_ corresponds to the delta between the column indexes of the current and next column. Columns having a larger delta are all assigned '0' probabilities. 

        - NOTE / Possible Enhancement : Perhaps a better way of assigning transition probabilites (instead of assigning zeros to columns with large deltas) would be to use an inverse weighted distribution (based on distance) or use the formula (1/distance)/sum(1/distance) to compute transition probabilities based on distance between columns. Unfortunately,we were unable to implement this due to time constraints. 

    3) Prior - 

        We used the element with maximum emission probability in the first column of our emission table to be our starting point.

- Let us now discuss the algorithms we used to obtain the boundaries - 

    1. Simplified Bayes net : 
        
        We were able to solve this relatively easily by obtaining the row index of the element having the max edge strength in each column and putting these all together to plot the boundaries.

    2. Viterbi : 

        The viterbi algorithm helps us obtain the boundary in a more accurate manner than the above approach as it takes into account the position of the next pixel and ensures that the pixel is relatively close by ( for boundary smoothness ) in addition to the edge strength. 

        We obtain the product of the maximum emission probability with the product of the max of the previous state and transition value. We also keep track of the max value of each of the previous states. In this way we create the dp table for viterbi. 

        We then backtrack from the max value from the last column to the max values we have stored so as to get the boundary.

    3. Viterbi + Human intervention : 

        To improve the results from the previous step we also use human input ( which is basically a point that is on the actual air-ice/ice-rock boundary ). We give every column a _zero_ probability in the emission probability except for the exact point given by the human which is set as _one_ in order to bias the program to move the boundary on/towards the given point which may make the output more correct. 

- Problems faced : 
    
    1. Using just the probabilites we faced underflow issues in our program, and so we multiplied probabilites by 10 in order to avoid this. We have also created a viterbi program tha makes use of the log domain in order to avoid this, but it was giving us very poor results for some reason. the function is present in our code and is called _viterbi log_   

- References : 

    1. https://towardsdatascience.com/probability-learning-vi-hidden-markov-models-fab5c1f0a31d

    2. https://www.audiolabs-erlangen.de/resources/MIR/FMP/C5/C5S3_Viterbi.html

- Output samples : 

    1. /Users/aditcam/Desktop/Assignment_Code/EAI/adcama-melmath-reddysai-a3/part2/Screen Shot 2021-12-01 at 8.52.47 PM.png






