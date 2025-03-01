"""
This script implements a k-Nearest Neighbors (k-NN) classifier to classify handwritten digits from the MNIST dataset.
The main steps are as follows:
1. Load training and test data from CSV files (MNIST_training.csv and MNIST_test.csv).
2. Separate features (pixel values) and labels (digit values) for both training and test sets.
3. Convert the data into NumPy arrays for efficient numerical operations.
4. Implement the k-NN algorithm:
   - For each test sample, calculate the Euclidean distance to all training samples.
   - Identify the k closest training samples (neighbors).
   - Determine the most common label among these neighbors and use it as the predicted label.
   - Compare the prediction with the ground truth label to measure accuracy.
5. Loop through different values of k (odd numbers from 1 to 19) to observe the effect on classification accuracy.
6. Print the number of correctly and incorrectly classified samples and the accuracy for each k value.

This implementation manually calculates distances and performs voting, rather than using a library function,
to provide an educational view of how the k-NN algorithm works under the hood.
"""

# Import necessary libraries
import pandas as pd  # For data manipulation and analysis
import matplotlib.pyplot as plt  # For data visualization (not used in this script but typically useful for plotting)
import numpy as np  # For numerical operations

# Read in the data from CSV files
# MNIST_training.csv: Contains labeled training data
# MNIST_test.csv: Contains labeled test data
trainingData = pd.read_csv('MNIST_training.csv')
testData = pd.read_csv('MNIST_test.csv')

# Separate labels (y) from features (x) in the training data
y = trainingData.iloc[:, 0]  # Labels (first column)
x = trainingData.drop('label', axis=1)  # Features (all other columns)

# Convert the training features to a NumPy array for faster calculations
SampleData = np.array(x.iloc[:], dtype=float)

# Extract labels from test data
y2 = testData.iloc[:, 0]  # Ground truth labels for test set

# Convert test labels to a NumPy array
ground_Truth = np.array(np.transpose(y2.values))

# Extract features from test data
x2 = testData.drop('label', axis=1)

# Initialize a list to store the predictions (optional, not used in accuracy calculation)
guessList = []

# Get the number of training samples
a = len(SampleData)

# Loop through odd values of k from 1 to 19 (for k-NN classifier)
# Odd values are used to avoid ties when voting among neighbors
for k in range(1, 20, 2):
    correct = 0  # Counter for correctly classified samples
    wrong = 0   # Counter for incorrectly classified samples
    
    # Loop through the first 50 test samples
    for i in range(0, 50, 1):
        # Extract the ith test sample
        TestD = x2.iloc[i, :]
        Testi = np.array(TestD, dtype=float)
        
        # Duplicate the test sample to match the number of training samples for vectorized calculation
        testi = np.tile(Testi, (a, 1))
        
        # Calculate the Euclidean distance between the test sample and all training samples
        # Formula: sqrt(sum((SampleData - TestSample)^2))
        tmpMatrix = np.sum(np.square(SampleData - testi), axis=1)
        tmpDistance = np.sqrt(tmpMatrix)
        
        # Get the labels of the k nearest neighbors
        kneighbors = y[np.argsort(tmpDistance)[:k]]
        
        # Determine the most common label among the k neighbors using voting
        tmp = np.bincount(kneighbors)
        guess = np.argmax(tmp)
        
        # Compare the predicted label with the true label
        if guess == y2[i]:
            correct += 1
        else:
            wrong += 1
    
    # Print the performance for the current value of k
    print("K value:", k)
    print("Correctly classified:", correct, "Incorrectly classified:", wrong)
    print("Accuracy:", correct / len(y2), "\n")

