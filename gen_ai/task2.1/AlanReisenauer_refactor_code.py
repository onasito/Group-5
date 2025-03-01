# Alan Reisenauer
# NSHE ID: 2001751827
# CS 422 Assignment 5
# Description: Program that implements a Logistic Regression model to solve a binary classification problem.
# For the same dataset as assignment 3
# Data set must be as follows:
#   - Number of input features: 3+
#   - Input characteristics:    Continuous Real-Valued
#   - Output characteristics:    Binary

# Data set I chose: https://www.kaggle.com/datasets/prishasawhney/mushroom-dataset
# Poisonous Mushrooms VS Edible Mushrooms
# Output = 0 - Edible | 1 - Poisonous
# Inputs (Columns L to R):
#       - Cap Diameter (cap-diameter)
#       - Cap Shape (cap-shape)
#       - Gill Attachment (gill-attachment)
#       - Gill Color (gill-color)
#       - Stem Height (stem-height)
#       - Stem Width (stem-width)
#       - Stem Color (stem-color)
#       - Season (season)
#       - Class (class)

# import the libraries used
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, f1_score, log_loss, confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# import the data file
# File path: "C:\Users\alanf\PycharmProjects\Assignment3\mushroom_cleaned.csv"
data = pd.read_csv('mushroom_cleaned.csv')

# check data is imported correctly
print(data)

# split up the data into 80% for training and 20% for testing
# split data up into input features and classes
X = data.drop('class', axis=1)
y = data['class']
input_features_train, input_features_test, outputs_train, outputs_test = train_test_split(X, y, test_size=0.2,
                                                                                          random_state=0)

# Experiment configurations
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


# Helper function to compute evaluation metrics
def compute_metrics(y_true, y_pred, y_prob):
    cm = confusion_matrix(y_true, y_pred, labels=[1, 0])

    # Extract confusion matrix values
    tp, fn, fp, tn = cm.ravel()

    # Compute key metrics
    accuracy = accuracy_score(y_true, y_pred)
    sensitivity = recall_score(y_true, y_pred, pos_label=1)  # True Positive Rate
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0  # True Negative Rate
    f1 = f1_score(y_true, y_pred)  # Directly use f1_score from sklearn
    logloss = log_loss(y_true, y_prob)

    return [accuracy, sensitivity, specificity, f1, logloss]


# Initialize a dictionary to store results
results = {"Training": {}, "Testing": {}}

# Run each experiment
for experiment in experiments:
    print(experiment["description"])

    # Initialize the model
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

    # Evaluate on training data
    trainPred = model.predict(input_features_train)
    trainProb = model.predict_proba(input_features_train)[:, 1]  # Take probability for class 1
    results["Training"][experiment["description"]] = compute_metrics(outputs_train, trainPred, trainProb)

    # Evaluate on testing data
    testPred = model.predict(input_features_test)
    testProb = model.predict_proba(input_features_test)[:, 1]  # Take probability for class 1
    results["Testing"][experiment["description"]] = compute_metrics(outputs_test, testPred, testProb)

# Convert results dictionary to DataFrame
columns = ['Accuracy', 'Sensitivity', 'Specificity', 'F1 Score', 'Log Loss']
train_df = pd.DataFrame(results["Training"], index=columns).T
test_df = pd.DataFrame(results["Testing"], index=columns).T

# Print tables
print("\nTraining Metrics:")
print(train_df)

print("\nTesting Metrics:")
print(test_df)
