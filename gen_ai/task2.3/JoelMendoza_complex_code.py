import pandas as pd
import numpy as np
from sklearn.model_selection import KFold

# Define the column names for the dataset
columns = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model year', 'origin']

# Load data from a CSV file and read it into a pandas DataFrame
data = pd.read_csv("auto-mpg2.csv", header=None, sep=',')

# Separate the target variable (mpg) from the rest of the data (features)
y = data.iloc[:, 0]  # 'mpg' is in the first column
X = data.drop(columns=[0, 8], axis=1)  # Drop the first column (mpg) and the last column (car name)
X.columns = columns  # Set column names for the features

# Standardize the features (X) to have a mean of 0 and standard deviation of 1
X_standardized = (X - X.mean()) / X.std()
X_standardized = pd.DataFrame(X_standardized, columns=X.columns)

def Linear_Regression(X, y):
    """
    Perform Linear Regression to calculate the model's coefficients (weights).

    This function uses the **Normal Equation** to compute the coefficients that minimize the squared error
    between the predicted and actual values of the target variable. It assumes that the feature matrix X
    is already preprocessed (including adding a column for the intercept term).

    The normal equation formula is:
    
        b = (X^T * X)^-1 * X^T * y
    
    Where:
        - X is the feature matrix (with a column of ones added for the intercept term).
        - b is the vector of coefficients (including the intercept).
        - y is the target variable (in this case, the mpg values).

    This approach is computationally efficient for small to medium-sized datasets, but may become slow or
    unstable with larger datasets or when the feature matrix X is ill-conditioned (e.g., highly correlated features).
    """
    # Add a column of ones for the intercept term (this is the "bias" in linear regression)
    X_inter = np.c_[np.ones((X.shape[0], 1)), X]
    
    # Apply the normal equation to calculate the coefficients
    coefficients = np.dot(np.dot(np.linalg.inv(np.dot(X_inter.transpose(), X_inter)), X_inter.transpose()), y)
    return coefficients

def RMSE(y_pred, y_true, n):
    """
    Calculate the Root Mean Squared Error (RMSE) between predicted and true values.

    RMSE is a common metric used to evaluate the performance of regression models. It measures the average
    magnitude of the error between the predicted and true values. The formula for RMSE is:

        RMSE = sqrt(sum((y_pred - y_true)^2) / n)

    Where:
        - y_pred: The predicted values from the model.
        - y_true: The true values of the target variable (in this case, the mpg values).
        - n: The number of data points (length of the dataset).

    A lower RMSE value indicates a better fit, with zero indicating a perfect prediction.
    """
    return np.sqrt(np.sum((y_pred - y_true) ** 2) / n)

RMSE_list = []  # List to store RMSE values for each fold of cross-validation

# Set up K-Fold cross-validation with 10 folds
KF = KFold(n_splits=10, shuffle=True, random_state=13)
fold_counter = 1  # Counter to keep track of the current fold number

# Add RMSE to the list of column headers to be displayed later
columns += ['RMSE'] 

# Print the column headers to display the output format
for header in columns: 
    print('\t\t', header, end=' ')
print()

# Loop through each fold in the K-Fold cross-validation
for train_index, test_index in KF.split(X_standardized):
    # Split the data into training and testing sets based on the current fold
    X_train  = X_standardized.iloc[train_index]
    X_test   = X_standardized.iloc[test_index]
    y_train  = y.iloc[train_index]
    y_test   = y.iloc[test_index]

    # Perform linear regression on the training data to get the coefficients
    b = Linear_Regression(X_train, y_train)
    
    # Use the coefficients to make predictions on the test data
    y_pred = np.dot(np.c_[np.ones((X_test.shape[0], 1)), X_test], b)

    # Calculate the RMSE for the current fold and add it to the RMSE list
    RMSE_vals = RMSE(y_pred, y_test, len(y_test))
    RMSE_list.append(RMSE_vals)

    # Print out the results for the current fold
    print(f"Fold: {fold_counter}")
    print("Coefficients:", b[1:], RMSE_list[fold_counter - 1], "\n")  # Display the coefficients (excluding the intercept) and the RMSE for this fold
    fold_counter += 1  # Move to the next fold

# Calculate and print the average RMSE over all folds
average_RMSE = np.mean(RMSE_list)
print(f"Average RMSE of all folds: {average_RMSE}")
