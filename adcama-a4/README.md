# a4

# Part 1 : K- Nearest Neighbors Classification

- The objective of this problem is to classify a new data point into one of the existing clusters/categories. The fundamental idea is to find the distance of the new datapoint from every other point in the dataset and based on the the k-nearest (k is usually chosen by the user) we make a decision on the classification, this decision can be made based in a couple of ways, two of which we have implemented and will discuss below. (inverse distance or uniform votes)


## Problem solving approach 

- There are 2 distance metrics we have used to compute the distance between 2 datapoints, they are as follows - 

    1) Euclidean distance :  For data points (x,y) of n-dimension is the squareroot of (x1-y1)^2 + (x2-y2)^2 + (x3-y3)^2 + ... + (xn-yn)^2.  I have used the np.linalg.norm to perform the same. 

    2) Manhattan distance : Also known as City block distance, for data points (x,y) of n-dimension is |x1-y1| + |x2-y2| + |x3-y4| + ... + |xn-yn|. I have used np.sum(np.abs(x1-x2)). 

- The next thing we do is compute the distance between every point in the dataset and the given data point whose class we have to predict. This is done by iteratively finding the distances and choosing the k nearest datapoints that are closest to the given datapoint. Based on these k points we now have to decide the final cluster prediction. This can be done in 2 ways - 

    1. Uniform : Select the label which is in majority amongst the k nearest neighbours. (In terms of a tie situatuion I arbitrarily choose the numerically smallest class label). Here each datapoint has 1 vote for the class it belongs to. 

    2. Distance : In this scenario we take an inverse of the distance of the given data points and sum it label-wise, this means that each label now has a number attached to it and we select the one with maximum inverse distance sum. In simpler terms, we give priority to neighbours that are nearer to the given data point instead of giving them an equal weightage as seen in the above scenario.  

## Observation 

- Our KNN model seems to be performing on par with the scikitlearn implementation of KNN in most scenarios, it is almost identical for the iris dataset. 
- In terms of the digits dataset our outputs were yet again identical about 80% of the time, however 20% of the time there was a 10-12% delta in terms of the accuracy between our model and the scikitlearn implementation. 

<hr>


# Part 2 : Multilayer Perceptron Classification

- The objective here is to use a collection of neurons (a computational unit) in a layered format to perform the classification tasks similar to the previous problem. 


## Problem solving approach 

- The multilayered neural network we are asked to implement is a neural with just 3 layers, namely the input layer, hidden layer and output layer, this is a fully connected neural network.

- We first implement some of the utility functions (mostly activation functions that shape our output in a certain manner) that would be necessary for our neural network, they are as follows -

    - *Identity activation function & it's derivative* : As evident from the name, this funciton essentially returns back the input. If the derivative flag is true it returns a vector of ones as the derivative of this function is one.  

    - *Sigmoid & it's derivative* : The sigmoid function is - F(x) = 1/1+e^(-x). It's derivative is sigmoid(x)*(1-sigmoid(x)).

    - *Tanh & it's derivative* : We use np.tanh(x) to compute the output for this activation function. It's derivative is (1-(tanh(x)^(2))).

    - *Relu & it's derivative* : The ReLU function returns 0 if the number is less than otr equal to zero, or the input if the input is >0 or +ve. its derivative is 1 if the number is positive and 0 in any other case.

    - *Softmax & it's derivative* : This is the function we use for the output layer for class prediction probability. (Pre-implemented for us).
    
    - *Cross entropy function*:  defined as the negative log-likelihood of a logistic model that returns
    p probabilities for its true class labels y. Here we take an element wise product of the one hot encoded vector of the target labels and the predicted probabilities of the softmax function. We then filter out entries with zeros as the next step is taking the sum of negative logs over all values and then finally taking a mean over the final output vector to obtain the crosss entropy loss value.

    - *One-hot encoding function *: This function converts a vector y of categorical target class values into a one-hot numeric array using one-hot encoding: one-hot encoding creates new binary-valued columns, each of which indicate the presence of each possible value from the original data.  

- The next step is to initialize the variables for the multilayer perceptron, this is done in the initialize function. Here we randomly initialize the hidden weights and biases & the output weights and biases. 

- The next step is to Train the neural network in order to obtain the appropriate weight and bias paramaters. For this we iteratively perform the feedforward and backpropogation steps (iteration count is decided by the user). In the feedforward step we essentialy calculate the input * weights + biases for  each layer and use that as the input to the next layers. In the backpropogation step we update the weights by taking a derivative of the loss function (and trying to minimize it using Stochiastic Gradient Descent, the learning rate alpha is provided by the user as well)

## Problems faced 

- The output of the cross entropy function was initally a vector in py understanding, but I then took a mean to get a singular values based on Q&A community. 
- The backpropogation step was challenging to implement and I was unable to fully complete the same.