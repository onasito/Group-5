
'''
    This code was for a CS 422 Machine Learning course.
    This code uses the MNIST_100 dataset which is a variation of the original MNIST dataset consisting of 100 handwritten numbers. 
'''
# Import necessary libraries
import pandas as pd  # For handling data in tabular form
import matplotlib.pyplot as plt  # For visualization
from sklearn.decomposition import PCA  # For Principal Component Analysis (PCA)

# Load the dataset
# The dataset is assumed to be in CSV format with the first column containing labels
data = pd.read_csv('MNIST_100.csv')

# Separate features (X) and labels (y)
y = data.iloc[:, 0]  # Extract labels (first column)
x = data.drop('label', axis=1)  # Remove the label column to retain only features

# Apply PCA for dimensionality reduction
pca = PCA(n_components=2)  # Reduce the data to 2 principal components
pca.fit(x)  # Compute the principal components
PCAX = pca.transform(x)  # Transform the original data into the new 2D PCA space

# Create a scatter plot to visualize the reduced data
fig, ax = plt.subplots()

# Define parameters for visualization
size_of_data = len(PCAX)  # Total number of data points
size_of_class = 100  # Assumed class size (100 samples per class)

# Loop through data and plot each class with a unique color
for i in range(0, size_of_data, size_of_class):
    ax.scatter(PCAX[i:i+size_of_class, 0], PCAX[i:i+size_of_class, 1], 
               label=i//size_of_class)  # Assign class labels based on index

# Add plot title and axis labels
ax.set_title("Task 1: Scatter plot of PCA")
ax.set_xlabel("Principal Component 1 (PC1)")
ax.set_ylabel("Principal Component 2 (PC2)")

# Add legend for class labels
ax.legend(loc='best', title='Classes', fontsize='xx-small')

# Display the plot
plt.show()