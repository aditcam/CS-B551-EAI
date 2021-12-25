#!/usr/local/bin/python3
#
# Authors: Sai Prajwal Reddy: reddysai@iu.edu, Aditya Camarushy: adcama@iu.edu, Melissa Rochelle Mathias: melmath@iu.edu
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import numpy as np
import math
import copy


# calculate "Edge strength map" of an image                                                                                                                                      
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image

def viterbi_log(edge_strength,emission,transition):

    emission = np.where(emission>0,np.log(emission),0)
    edge_strength = np.where(edge_strength>0,np.log(edge_strength),0)

    max_val_ind = []
    result = []
    prob = {0 : emission[0]}

    col_count = edge_strength.shape[0]

    for i in range(edge_strength.shape[1]):

        lst = []
        tmp = []

        for j in range(col_count):
            
            # create transition vector

            trans = np.zeros(col_count)

            if j<=col_count-5 and j>=5:
                for k in range(j-5,j+5,1):
                    trans[k] = transition[abs(j-k)]
            elif j<5:
                for k in range(0,j+5,1):
                    trans[k] = transition[abs(j-k)]
            else:
                for k in range(j-5,col_count,1):
                    trans[k] = transition[abs(j-k)]

            prob_prod = prob[i] + trans
            tmp.append(np.argmax(prob_prod))
            lst.append(emission[i][j]+max(prob_prod))
        max_val_ind.append(tmp)
        prob[i+1] = np.array(lst)

    # Backtracking step

    prev_max_val_index = np.argmax(prob[edge_strength.shape[1]])

    for i in range(len(max_val_ind)-1,-1,-1):
        result.append(max_val_ind[i][prev_max_val_index])
        prev_max_val_index = max_val_ind[i][prev_max_val_index]
    
    return result[::-1]

def viterbi(edge_strength,emission,transition):

    # emission = np.where(emission>0,np.log(emission),0)
    # edge_strength = np.where(edge_strength>0,np.log(edge_strength),0)

    max_val_ind = []
    result = []
    prob = {0 : emission[0]}

    col_count = edge_strength.shape[0]

    for i in range(edge_strength.shape[1]):

        lst = []
        tmp = []

        for j in range(col_count):
            
            # create transition vector

            trans = np.zeros(col_count)
            # if j<=col_count-5 and j>=5: 
            #     trans[j-5:j+6] = transition
            # elif j<5:
            #     # trans[j:j+6] = transition
            #     # print(trans)
            #     # print(transition)
            #     # for k in range(j):
            #     #     trans[j] = transition[]
            #     trans[0:5-j]
            # else:
            #     # trans[j-5:j] = transition[:0:-1]
            #     # trans[j:col_count] = transition[:col_count-j]

            if j<=col_count-5 and j>=5:
                for k in range(j-5,j+5,1):
                    trans[k] = transition[abs(j-k)]
            elif j<5:
                for k in range(0,j+5,1):
                    trans[k] = transition[abs(j-k)]
            else:
                for k in range(j-5,col_count,1):
                    trans[k] = transition[abs(j-k)]

            prob_prod = prob[i] * trans
            tmp.append(np.argmax(prob_prod))
            lst.append(emission[i][j]*max(prob_prod))
        max_val_ind.append(tmp)
        prob[i+1] = np.array(lst)

    # Backtracking step

    prev_max_val_index = np.argmax(prob[edge_strength.shape[1]])

    for i in range(len(max_val_ind)-1,-1,-1):
        result.append(max_val_ind[i][prev_max_val_index])
        prev_max_val_index = max_val_ind[i][prev_max_val_index]
    
    return result[::-1]


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)

# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]

    # load in image 
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # You'll need to add code here to figure out the results! For now,
    # just create some random lines.

    ######### SIMPLE #########

    # ------------------------------------------------------------------------------------------------------------------------ #

    edge_strength_1 = np.array(edge_strength) # convert to numpy array
    edge_strength_1 = edge_strength_1.T # Transpose is performed so as to store the data column-wise so as to make lcolumnwise manipulations easier later on
    airice_simple = np.argmax(edge_strength_1,axis=1) # Get the maximum value each column to get the y coordinates to plot the boundary
    airice_simple+=2 # Adding 2 to the numpy array so as to make the bring down the y coordinates pixel values to center the plot line between the boundary 
    
    icerock_simple = []
    
    for i in range(len(edge_strength_1)):
        icerock_simple.append(np.argmax(edge_strength_1[i][airice_simple[i]+10:])+airice_simple[i]+10)

    # ------------------------------------------------------------------------------------------------------------------------ #

    ######### HMM ######### 

    # ------------------------------------------------------------------------------------------------------------------------ #

    # Create Emission & Prior Probabilities

    # NOTE : WE MULTIPLY THE PROBABILITIES BY 10 SO AS TO PREVENT ARITHMETIC UNDERFLOW

    col_sum = np.sum(edge_strength_1,axis=1)

    emission = edge_strength_1/col_sum.reshape(-1,1) # computing the emission probability by dividing the edge strength of a given column by the sum of the edge strengths across the entire column
    emission = emission * 10 

    # Create transition probabilities

    # we will consider ± 5 rows when transitioning from one column to another, therefore we assign probabilities normalized to 1 and we also multiplied the probabilities by 10 to prevent arithmetic underflow errors 

    transition_prob = np.array([0.25,0.2,0.1,0.05,0.0175,0.0075])
    # transition_prob = np.array([100,50,25,12.5,6.25,3.125,1.625,0.78125,0.390,0.19,0.097])
    # transition_prob/=100
    # transition_prob = np.where(transition_prob>0, np.log(transition_prob), 0)
    transition = {}
    transition_prob*=10
    for i in range(6):
         transition[i] = transition_prob[i]

    # ********************* Air - Ice HMM Viterbi ***************************

    airice_hmm = np.array(viterbi(edge_strength,emission,transition))
    airice_hmm+=2

    # ********************* Ice - Rock HMM + Viterbi **************************

    edge_strength_2 = copy.deepcopy(edge_strength_1)

    for i in range(len(edge_strength_2)):
        edge_strength_2[i][:airice_hmm[i]+30] = np.zeros(airice_hmm[i]+30)

    col_sum = np.sum(edge_strength_2,axis=1)

    emission_1 = edge_strength_2/col_sum.reshape(-1,1)
    
    emission_1 = emission_1 * 10

    edge_strength_2 = edge_strength_2.T

    icerock_hmm = np.array(viterbi(edge_strength_2,emission_1,transition))
    icerock_hmm+=2

    # ------------------------------------------------------------------------------------------------------------------------ #

    ######### Human Feedback + Viterbi #########

    # ------------------------------------------------------------------------------------------------------------------------ #

    # ********************* Air - Ice Human Feedback + Viterbi **************************

    emission_2 = copy.deepcopy(emission)
    emission_2[:,int(gt_airice[1])] = 0
    emission_2[int(gt_airice[0]),int(gt_airice[1])] = 10

    airice_feedback = np.array(viterbi(edge_strength,emission_2,transition))
    airice_feedback+=2

    edge_strength_3 = copy.deepcopy(edge_strength_1)

    # ********************* Ice - Rock Human Feedback + Viterbi **************************
    
    for i in range(len(edge_strength_3)):
        edge_strength_3[i][:airice_feedback[i]+30] = np.zeros(airice_feedback[i]+30)

    col_sum = np.sum(edge_strength_3,axis=1)

    emission_3 = copy.deepcopy(emission)
    emission_3 = edge_strength_3/col_sum.reshape(-1,1)
    
    emission_3 = emission_3 * 10

    edge_strength_3 = edge_strength_3.T

    emission_3[:,int(gt_icerock[1])] = 0
    emission_3[int(gt_icerock[0]),int(gt_icerock[1])] = 10

    icerock_feedback = np.array(viterbi(edge_strength_3,emission_3,transition))
    icerock_feedback+=2

    # icerock_feedback= [ image_array.shape[0]*0.75 ] * image_array.shape[1]
    # airice_feedback = [ image_array.shape[0]*0.75 ] * image_array.shape[1]

    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
