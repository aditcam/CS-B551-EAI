#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# Aditya Shekhar Camarushy : adcama
# Melissa Rochelle Mathias : melmath
# Sai Prajwal reddy : reddysai 
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import re
import math 

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    #print(im.size)
    #print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    #print(result[0])
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!


# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
#print("\n".join([ r for r in train_letters['a'] ]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
#print("\n".join([ r for r in test_letters[2] ]))



# The final two lines of your output should look something like this:
#print("Simple: " + "Sample s1mple resu1t")
#print("   HMM: " + "Sample simple result") 

#Calculating the Initial and Transitional Probability 
initial_prob = {}
transition = {}
with open(train_txt_fname,'r') as f:
    for line in f:
        letters_list = list(re.sub(r'[^\w\s]',r' ',' '.join([letter for letter in line.split()][0::2])))
        if letters_list:
            if letters_list[0] in initial_prob.keys():
                initial_prob[letters_list[0]] += 1
            else:
                initial_prob[letters_list[0]] = 1
            for letter_index in range(1,len(letters_list)):
                if letters_list[letter_index-1] in transition.keys():
                    if letters_list[letter_index] in transition[letters_list[letter_index-1]].keys():
                        transition[letters_list[letter_index-1]][letters_list[letter_index]] += 1
                    else:
                        transition[letters_list[letter_index-1]][letters_list[letter_index]] = 1
                else:
                    transition[letters_list[letter_index-1]] = {letters_list[letter_index] : 1}
        total_sum = sum(initial_prob.values())
    for prob in initial_prob.keys():
        initial_prob[prob] = initial_prob[prob]/total_sum
    for letter1 in transition:
        transition_sum = sum(transition[letter1].values())
        for letter2 in transition[letter1]:
            transition[letter1][letter2] = transition[letter1][letter2]/transition_sum

#Calculating the emission probability
emission = {}
black_count_test = 0
black_count_train = 0
for index in range(0,len(test_letters)):
    emission[index] =  {}
    for letter in train_letters:
        black = 0
        white = 0
        no_match_black = 0
        no_match_white = 0
        for character in train_letters[letter]:
            if character == '*':
                black_count_train+=1
        for char_index in range(len(test_letters[index])):
            if test_letters[index][char_index] == '*':
                black_count_test+=1
            for i in range(0,len(test_letters[index][char_index])):
                if (test_letters[index][char_index][i] == train_letters[letter][char_index][i]):
                    if (train_letters[letter][char_index][i] == '*'):
                        black+=1
                    elif (train_letters[letter][char_index][i] == ' '):
                        white+=1
                elif (train_letters[letter][char_index][i] == '*'):
                    no_match_black+=1
                elif (train_letters[letter][char_index][i] == ' '):
                    no_match_white+=1
        if black_count_test/len(test_letters) > black_count_train/len(train_letters):
            emission[index][letter] = ((0.75 ** black) * (0.75 ** white) * (0.25 ** no_match_black) * (0.25 ** no_match_white))
        else:
            emission[index][letter] = ((0.97 ** black) * (0.75 ** white) * (0.25 ** no_match_black) * (0.03 ** no_match_white))
#For simplified method
simple = ''
for prob in emission:
    simple += ''.join(max(emission[prob],key = lambda x: emission[prob][x]))
print("Simple: " + simple)

#HMM Viterbi
current_letter = [None] * 128
previous_letter = [None] * 128
for test_index,test_letter in enumerate(test_letters):
    for train_index,train_letter in enumerate(train_letters):
        if test_index == 0:
            hmmv = -math.log(emission[0][train_letter]) - (math.log(initial_prob[train_letter] if train_letter in initial_prob.keys() else 0.000000001))
            current_letter[ord(train_letter)] = [hmmv,[train_letter]]
        else:
            temp = []
            for p_index,p_char in enumerate(train_letters):
                if p_char in transition.keys():
                    trans_prev_prob = (-math.log(transition[p_char][train_letter] if train_letter in transition[p_char].keys() else 0.000000001)) + previous_letter[ord(p_char)][0]
                else:
                    trans_prev_prob = (-math.log({}[train_letter] if train_letter in {}.keys() else 0.000000001)) + previous_letter[ord(p_char)][0]

                temp.append([trans_prev_prob,previous_letter[ord(p_char)][1] + [train_letter]])
            previous_max_value = min(temp)
            hmmv = previous_max_value[0] - math.log(emission[test_index][train_letter])
            current_letter[ord(train_letter)] = [hmmv,previous_max_value[1]]
    previous_letter = current_letter
    current_letter = [None] * 128
temp_hmmv = [element for element in previous_letter if element is not None]
hmmv = min(temp_hmmv)
print("   HMM: " + ''.join(hmmv[1]))