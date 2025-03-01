############################################################
# Logistic Regression Model for Binary Classification
# Author: Alan Reisenauer
# NSHE ID: 2001751827
# CS 422 - Assignment 5
############################################################
#
# Description:
# This program implements a Logistic Regression model using a Multi-layer Perceptron (MLP) to solve
# a binary classification problem. It evaluates different neural network configurations on a dataset
# to classify mushrooms as either edible or poisonous.
#
# Dataset:
# - Source: https://www.kaggle.com/datasets/prishasawhney/mushroom-dataset
# - Target Variable: 'class' (0 = Edible, 1 = Poisonous)
# - Features:
#     - Cap Diameter (cap-diameter)
#     - Cap Shape (cap-shape)
#     - Gill Attachment (gill-attachment)
#     - Gill Color (gill-color)
#     - Stem Height (stem-height)
#     - Stem Width (stem-width)
#     - Stem Color (stem-color)
#     - Season (season)
#
# Model Evaluation Metrics:
# - Accuracy: Measures overall correctness of predictions.
# - Sensitivity (Recall): Measures how well the model detects positive cases (poisonous mushrooms).
# - Specificity: Measures how well the model detects negative cases (edible mushrooms).
# - F1 Score: Balances precision and recall.
# - Log Loss: Measures the probability confidence of predictions.
#
############################################################

# Import required libraries
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, f1_score, log_loss, confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Load dataset from file
# File path: "C:\\Users\\alanf\\PycharmProjects\\Assignment3\\mushroom_cleaned.csv"
data = pd.read_csv('mushroom_cleaned.csv')

# Display dataset structure
print(data.head())

# Split dataset into features (X) and target variable (y)
X = data.drop('class', axis=1)  # Feature variables
y = data['class']  # Target variable

# Split data into training (80%) and testing (20%) sets
input_features_train, input_features_test, outputs_train, outputs_test = train_test_split(
    X, y, test_size=0.2, random_state=0)

# Experiment configurations: Different neural network architectures
experiments = [
    {
        "description": "Experiment 1: Default Configuration",
        "hidden_layer_sizes": (100,),
        "activation": 'relu',
        "solver": 'adam',
        "learning_rate_init": 0.001,
    },
    {
        "description": "Experiment 2: Two Hidden Layers with Sigmoid Activation",
        "hidden_layer_sizes": (50, 30),
        "activation": 'logistic',
        "solver": 'adam',
        "learning_rate_init": 0.01,
    },
    {
        "description": "Experiment 3: Larger Network with Tanh Activation",
        "hidden_layer_sizes": (200, 100),
        "activation": 'tanh',
        "solver": 'sgd',
        "learning_rate_init": 0.01,
    }
]


# Function to compute evaluation metrics
def compute_metrics(y_true, y_pred, y_prob):
    """
    Compute classification evaluation metrics based on model predictions.
    :param y_true: Actual labels
    :param y_pred: Predicted labels
    :param y_prob: Predicted probabilities
    :return: List of computed metrics [accuracy, sensitivity, specificity, f1, logloss]
    """
    cm = confusion_matrix(y_true, y_pred, labels=[1, 0])
    tp, fn, fp, tn = cm.ravel()

    accuracy = accuracy_score(y_true, y_pred)
    sensitivity = recall_score(y_true, y_pred, pos_label=1)  # True Positive Rate
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0  # True Negative Rate
    f1 = f1_score(y_true, y_pred)
    logloss = log_loss(y_true, y_prob)

    return [accuracy, sensitivity, specificity, f1, logloss]


# Dictionary to store results
results = {"Training": {}, "Testing": {}}

# Run experiments with different configurations
for experiment in experiments:
    print(f"Running: {experiment['description']}")

    # Initialize MLPClassifier with experiment parameters
    model = MLPClassifier(
        hidden_layer_sizes=experiment["hidden_layer_sizes"],
        activation=experiment["activation"],
        solver=experiment["solver"],
        learning_rate_init=experiment["learning_rate_init"],
        max_iter=1000,
        random_state=0
    )

    # Train the model
    model.fit(input_features_train, outputs_train)

    # Evaluate model on training data
    train_pred = model.predict(input_features_train)
    train_prob = model.predict_proba(input_features_train)[:, 1]  # Probability of class 1
    results["Training"][experiment["description"]] = compute_metrics(outputs_train, train_pred, train_prob)

    # Evaluate model on testing data
    test_pred = model.predict(input_features_test)
    test_prob = model.predict_proba(input_features_test)[:, 1]  # Probability of class 1
    results["Testing"][experiment["description"]] = compute_metrics(outputs_test, test_pred, test_prob)

# Convert results dictionary to pandas DataFrame
columns = ['Accuracy', 'Sensitivity', 'Specificity', 'F1 Score', 'Log Loss']
train_df = pd.DataFrame(results["Training"], index=columns).T
test_df = pd.DataFrame(results["Testing"], index=columns).T

# Print training and testing results
print("\nTraining Metrics:")
print(train_df)

print("\nTesting Metrics:")
print(test_df)
