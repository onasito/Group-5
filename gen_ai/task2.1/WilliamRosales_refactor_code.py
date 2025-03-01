# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Task 1: Load and preprocess MNIST dataset
# Load the MNIST data from the CSV file
mnist_data = pd.read_csv('MNIST_100.csv')

# Separate the labels and features
labels = mnist_data['label']
features = mnist_data.drop('label', axis=1)

# Display the shape of the features and labels
print(f"Features shape: {features.shape}")
print(f"Labels shape: {labels.shape}")

# Perform PCA to reduce dimensions to 2 components
pca = PCA(n_components=2)
pca.fit(features)
features_pca = pca.transform(features)

# Plot the PCA-transformed data, grouping by labels (0-9)
fig, ax = plt.subplots(figsize=(10, 8))

for digit in range(10):
    # Get indices for the current digit
    indices = labels == digit
    # Scatter plot for each digit
    ax.scatter(features_pca[indices, 0], features_pca[indices, 1], label=digit)

# Add legend and title to the plot
ax.legend(title="Digits")
ax.set_title("PCA of MNIST Digits (2 Components)")
ax.set_xlabel("Principal Component 1")
ax.set_ylabel("Principal Component 2")

# Show the plot
plt.show()
