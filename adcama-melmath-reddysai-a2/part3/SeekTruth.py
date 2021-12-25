# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
# Aditya Shekhar Camarushy : adcama
# Melissa Rochelle Mathias : melmath
# Sai Prajwal reddy : reddysai 
# Based on skeleton code by D. Crandall, October 2021
#

import sys

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
import re
def classifier(train_data, test_data):
    all_words = {}
    for review in range(0,len(train_data['objects'])):
        train_data['objects'][review] = re.sub(r'[^\w\s]', ' ', train_data['objects'][review])
        for word in train_data['objects'][review].strip().lower().split():
            if word not in all_words and train_data['labels'][review] == 'truthful':
                all_words[word] = (1,0)
            elif word not in all_words and train_data['labels'][review] == 'deceptive':
                all_words[word] = (0,1)
            elif word in all_words and train_data['labels'][review] == 'truthful':
                t_count,d_count = all_words[word]
                all_words.update({word:(t_count+1,d_count)})
            elif word in all_words and train_data['labels'][review] == 'deceptive':
                t_count,d_count = all_words[word]
                all_words.update({word:(t_count,d_count+1)})
    prob_words = {}
    for review in range(0,len(test_data)):
        test_data['objects'][review] = re.sub(r'[^\w\s]', '', test_data['objects'][review])
    for word in all_words:
        t_count,d_count = all_words[word]
        prob_words.update({word:((t_count/(t_count+d_count)),(d_count/(t_count+d_count)))})

    truth_prob = train_data['labels'].count('truthful')/len(train_data['labels'])
    decept_prob = train_data['labels'].count('deceptive')/len(train_data['labels'])

    result = []

    for review in test_data['objects']:
        prob_t = truth_prob
        prob_d = decept_prob
        for word in review.strip().lower().split():
            if word in prob_words.keys():
                t_prob,d_prob = prob_words[word]
                if t_prob != 0 and d_prob != 0:
                    prob_t *= t_prob
                    prob_d *= d_prob
            else:
                continue
        if prob_t/prob_d > 1:
            result.append('truthful')
        else:
            result.append('deceptive')
    return result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
