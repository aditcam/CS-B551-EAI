###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names and user ids:
# Aditya Shekhar Camarushy : adcama
# Melissa Rochelle Mathias : melmath
# Sai Prajwal reddy : reddysai 
# (Based on skeleton code by D. Crandall)
#

import random
import math

#Dictionaries for counting
total_words = 0
word_count = {}
pos_count = {}
word_pos_count = {}
pos_word_count = {}
pos_pos_count = {}
starting_pos_count = {}
#Dictionaries for probabilities
word_prob = {}
pos_prob = {}
word_pos_prob = {}
pos_word_prob = {}
pos_pos_prob = {}
starting_pos_prob = {}

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        emissions_prob = 1
        transitions_prob = 1
        for i in range(len(sentence)):
            emissions_prob *= (pos_word_prob[label[i]].get(sentence[i],0.000001)/ pos_count[label[i]])
        for i in range(len(sentence)-1):
            transitions_prob *= (pos_pos_prob[label[i]].get(label[i-1],0.0001)) 
        return math.log(emissions_prob*transitions_prob + (10**(-20)))
       

    # Do the training!
    #
    
    def train(self, data):
        total_words = 0
        for i in data:
            total_words += len(i[0])
            for j in range(0,len(i[0])):
                if i[0][j] in word_count.keys():
                    word_count[i[0][j]] += 1
                else:
                    word_count[i[0][j]] = 1
                    word_pos_count[i[0][j]] = {}
                if i[1][j] in pos_count.keys():
                    pos_count[i[1][j]] += 1
                else:
                    pos_count[i[1][j]] = 1
                    pos_word_count[i[1][j]] = {}
                    pos_pos_count[i[1][j]] = {}
                if word_pos_count[i[0][j]].__contains__(i[1][j]):
                    word_pos_count[i[0][j]][i[1][j]] += 1
                else:
                    word_pos_count[i[0][j]][i[1][j]] = 1
                if pos_word_count[i[1][j]].__contains__(i[0][j]):
                    pos_word_count[i[1][j]][i[0][j]] += 1
                else:
                    pos_word_count[i[1][j]][i[0][j]] = 1
                if j < len(i[0])-1:
                    if pos_pos_count[i[1][j]].__contains__(i[1][j+1]):
                        pos_pos_count[i[1][j]][i[1][j+1]] += 1
                    else:
                        pos_pos_count[i[1][j]][i[1][j+1]] = 1
                if j == 0:
                    if i[1][j] in starting_pos_count.keys():
                        starting_pos_count[i[1][j]] += 1
                    else:
                        starting_pos_count[i[1][j]] = 1
        for i in word_count.keys():
            word_prob[i] = word_count[i]/total_words
            word_pos_prob[i] = {}
        for i in pos_count.keys():
            pos_prob[i] = pos_count[i]/total_words
            pos_word_prob[i] = {}
            pos_pos_prob[i] = {}
        for i in word_pos_prob.keys():
            for j in word_pos_count[i].keys():
                word_pos_prob[i][j] = word_pos_count[i][j]/word_count[i]
        for i in pos_word_prob.keys():
            for j in pos_word_count[i].keys():
                pos_word_prob[i][j] = pos_word_count[i][j]/pos_count[i]
        for i in pos_pos_prob.keys():
            for j in pos_pos_count[i].keys():
                pos_pos_prob[i][j] = pos_pos_count[i][j]/(pos_count[i])
        for i in starting_pos_count.keys():
            starting_pos_prob[i] = starting_pos_count[i]/len(data)
    
    #Simplified method
    def simplified(self, sentence):
        pos_list = list(pos_count.keys())
        result = ['noun'] * len(sentence)
        for i in range(0,len(sentence)):
            prob = 0
            if sentence[i] in word_pos_prob.keys():
                for j in range(0,len(pos_list)):
                    if word_pos_prob[sentence[i]].get(pos_list[j],0) > prob:
                        prob = word_pos_prob[sentence[i]][pos_list[j]]
                        result[i] = pos_list[j]
        return result

    #HMM Viterbi
    def hmm_viterbi(self,sentence):
        result = []
        prob= []
        pos_list = list(pos_count.keys())
        for index,word in enumerate(sentence):
            prob.append({})
            for pos in pos_list:
                #Getting the emission probability 
                e_prob = (pos_word_count[pos][word] if pos_word_count[pos].__contains__(word) else 0.000001)/ (pos_count[pos])
                if index == 0: #For the POS at the beginning of the sentence.
                    prob[index][pos] = {'prob': e_prob * (starting_pos_prob[pos] if starting_pos_prob.__contains__(pos) else 0.01),'prev_pos':None}
                else: #For the remaining part of the sentence.
                    temp = {}
                    for p in pos_list:
                        temp[p] = (prob[index-1][p]['prob'] * pos_pos_prob[p][pos] if pos_pos_prob[p].__contains__(pos) else prob[index-1][pos]['prob'] * 0.0001)
                        max_val,max_pos = max(zip(temp.values(),temp.keys()))
                        prob[index][pos] = {'prob':e_prob * max_val,'prev_pos':max_pos}
        max_prob = max(x['prob'] for x in prob[-1].values())
        prev = None
        for pos, values in prob[-1].items():
            if values['prob'] == max_prob:
                result.append(pos)
                prev = pos
                break
        for index in range(len(prob)-2,-1,-1):
            result.insert(0,prob[index+1][prev]['prev_pos'])
            prev = prob[index+1][prev]['prev_pos']
        return result
        #return [ "noun" ] * len(sentence)
    
    #MCMC Method Using Gibbs Sampling Algorithm
    #Referenced the approach from 'https://www.youtube.com/watch?v=yApmR-c_hKU' 
    #Referenced the approach from 'https://github.com/surajgupta-git/Artificial-Intelligence-projects/blob/main/POS%20Tagging/pos_solver.py'
    #Referenced the approach from 'https://www.youtube.com/watch?v=KmqTrm-bn8k&list=PLvcbYUQ5t0UEkf2NUEo7XSsyVTyeEk3Gq&index=6'
    #Referenced the approach from 'https://www.youtube.com/watch?v=7LB1VHp4tLE&list=PLvcbYUQ5t0UEkf2NUEo7XSsyVTyeEk3Gq&index=7'
    #Referenced the approach from 'https://www.youtube.com/watch?v=MNHIbOqH3sk&list=PLvcbYUQ5t0UEkf2NUEo7XSsyVTyeEk3Gq&index=8'
    def complex_mcmc(self, sentence):
        pos_list = list(pos_count.keys()) #Getting the list of different types of part of speech tags.
        random_value = self.simplified(sentence) #Getting a random speech tag using the simple method.
        result = {} 
        for count in range(100): #Running 100 iterations
            for index in range(len(sentence)):
                word = sentence[index] #Getting word from the test sentence
                temp_prob = [] #Storing all the probabilities after calculation
                if len(sentence) == 1: #If the sentence has only one word
                    for pos in pos_list:
                        prob = [math.log(word_pos_prob[word][pos] if word in word_pos_prob.keys() and pos in word_pos_prob[word].keys() else 0.00000001) +
                        math.log(starting_pos_prob[pos] if pos in starting_pos_prob.keys() else 0.000000001) ]
                        for i in prob:
                            temp_prob.append(i)
                elif index == 0: #For the POS in the beginning of the sentence
                    for pos in pos_list:
                        prob = [math.log(word_pos_prob[word][pos] if word in word_pos_prob.keys() and pos in word_pos_prob[word].keys() else 0.00000001) +
                        math.log(starting_pos_prob[pos] if pos in starting_pos_prob.keys() else 0.000000001) 
                        + math.log(pos_pos_prob[pos][random_value[index+1]] if pos in pos_pos_prob.keys() and random_value[index+1] in pos_pos_prob[pos].keys() else 0.000000001)]
                        for i in prob:
                            temp_prob.append(i)
                elif index == len(random_value) - 1 : #For the POS at the end of the sentence
                    for pos in pos_list:
                        prob = [math.log(word_pos_prob[word][pos] if word in word_pos_prob.keys() and pos in word_pos_prob[word].keys() else 0.000000001) +
                        math.log(pos_pos_prob[random_value[index-1]][random_value[0]] if random_value[index-1] in pos_pos_prob.keys() and random_value[0] in pos_pos_prob[random_value[index-1]].keys() else 0.0000000001) +
                        math.log(word_pos_prob[sentence[index]][random_value[index -1]] if sentence[index] in word_pos_prob.keys() and random_value[index-1] in word_pos_prob[sentence[index]].keys() else 0.0000000001) +
                        math.log(pos_pos_prob[pos][random_value[index -1]] if pos in pos_pos_prob.keys() and random_value[index-1] in pos_pos_prob[pos].keys() else 0.000000000001)]
                        for i in prob:
                            temp_prob.append(i)
                else:
                    for pos in pos_list: #Fot all the remaining in the sentence i.e in the middle.
                        prob = [math.log(word_pos_prob[sentence[index]][pos] if sentence[index] in word_pos_prob.keys()  and pos in word_pos_prob[word].keys() else 0.00000001) +
                        math.log(word_pos_prob[sentence[index-1]][random_value[index-1]] if sentence[index-1] in word_pos_prob.keys() and random_value[index-1] in word_pos_prob[sentence[index-1]].keys() else 0.00000001) +
                        math.log(word_pos_prob[sentence[index]][random_value[index-1]] if sentence[index] in word_pos_prob.keys() and random_value[index-1] in word_pos_prob[sentence[index]].keys() else 0.000000001) +
                        math.log(word_pos_prob[sentence[index+1]][random_value[index]] if sentence[index+1] in word_pos_prob.keys() and random_value[index] in word_pos_prob[sentence[index+1]].keys() else 0.000000001) +
                        math.log(word_pos_prob[sentence[index+1]][random_value[index+1]] if sentence[index+1] in word_pos_prob.keys() and random_value[index+1] in word_pos_prob[sentence[index+1]].keys() else 0.000000001) +
                        math.log(pos_pos_prob[random_value[index-1]][pos] if random_value[index-1] in pos_pos_prob.keys() and pos in pos_pos_prob[random_value[index-1]] else 0.000000001) +
                        math.log(pos_pos_prob[pos][random_value[index+1]] if pos in pos_pos_prob.keys() and random_value[index+1] in pos_pos_prob[pos].keys() else 0.0000000001)]
                        for i in prob:
                            temp_prob.append(i)
                exp_list = []
                for i in temp_prob:
                    exp_list.append(math.exp(i))
                #exp_sum = sum(exp_list)
                prob_list = [x/sum(exp_list) for x in exp_list]
                random_flip = random.uniform(0,1) #Getting a random flip
                max_prob= 0
                for p in range(len(prob_list)):
                    max_prob += prob_list[p]
                    if random_flip < max_prob :
                        random_value[index] = pos_list[p]
                        break
                for i in range(len(random_value)):
                    if(i,random_value[i]) not in result:
                        result[i,random_value[i]] = 1
                    else:
                        result[i,random_value[i]] += 1
        pos_tag = []
        for i in range(len(random_value)):
            max_prob = 0
            r_pos = ''
            for pos in pos_list:
                if (i,pos) in result:
                    if max_prob <= result[i,pos]:
                        max_prob = result[i,pos]
                        r_pos = pos
            pos_tag.append(r_pos)
        return pos_tag 
        #return [ "noun" ] * len(sentence)



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")