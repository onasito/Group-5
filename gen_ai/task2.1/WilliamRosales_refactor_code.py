# Import necessary libraries
import pandas as pd                 # For data manipulation
import matplotlib.pyplot as plt      # For data visualization
from sklearn.decomposition import PCA  # For dimensionality reduction

# Load the MNIST dataset from a CSV file
# The dataset is expected to have a 'label' column for digit labels (0-9)
# and other columns representing pixel values of the images.
mnist_dataframe = pd.read_csv('MNIST_100.csv')

# Separate the target labels (digits 0-9) from the pixel feature data
# The first column is the label (digit), and the remaining columns are pixel values.
digit_labels = mnist_dataframe.iloc[:, 0]  # Extract labels (target variable)
pixel_features = mnist_dataframe.drop('label', axis=1)  # Drop label column to get features

# Display the shape of the feature and label data
# This helps verify the dimensions of the input data.
print("Shape of pixel features:", pixel_features.shape)  # Expected: (1000, 784) for 1000 images, 784 pixels each
print("Shape of digit labels:", digit_labels.shape)      # Expected: (1000,) for 1000 labels

# Perform Principal Component Analysis (PCA) to reduce dimensionality to 2 components
# PCA helps in visualizing high-dimensional data by projecting it onto a 2D plane.
pca_model = PCA(n_components=2)  # Instantiate PCA model to reduce to 2 principal components
pca_model.fit(pixel_features)    # Fit the model on the pixel features

# Transform the pixel features to the 2D PCA space
# The transformed data will have 2 columns corresponding to the 2 principal components.
reduced_features_2d = pca_model.transform(pixel_features)

# Create a scatter plot to visualize the data in the 2D PCA space
fig, scatter_plot = plt.subplots()  # Create a figure and axes for the scatter plot

# Define the number of digit classes (0-9) and samples per class
num_classes = 10
samples_per_class = 100  # Assuming 100 samples for each digit class (0-9)

# Plot the data points for each digit class (0-9) with different colors and labels
# This loop groups and colors the data points by their digit labels.
for digit in range(num_classes):
    # Calculate the index range for the current digit class
    start_index = digit * samples_per_class  # Start index for the current digit class
    end_index = start_index + samples_per_class  # End index for the current digit class

    # Scatter plot for the current digit class in the 2D PCA space
    # PC1 (x-axis) vs PC2 (y-axis)
    scatter_plot.scatter(
        reduced_features_2d[start_index:end_index, 0],  # Principal Component 1
        reduced_features_2d[start_index:end_index, 1],  # Principal Component 2
        label=f"Digit {digit}"  # Label for the legend
    )

# Add legend, title, and axis labels to the plot
# This improves the readability and interpretability of the plot.
scatter_plot.legend(title="Digits")            # Legend to identify each digit class
plt.title("PCA Visualization of MNIST Digits") # Title of the plot
plt.xlabel("Principal Component 1")            # Label for x-axis
plt.ylabel("Principal Component 2")            # Label for y-axis
plt.grid(True)                                 # Add a grid to the plot for better visualization
plt.show()                                     # Display the scatter plot
