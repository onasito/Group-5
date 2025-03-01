import ssl
import numpy as np
import pandas as pd
from ucimlrepo import fetch_ucirepo
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, f1_score, log_loss, confusion_matrix

# disable SSL verification to bypass the certtification error
ssl._create_default_https_context = ssl._create_unverified_context

# fetch dataset
skin_segmentation = fetch_ucirepo(id=229)

# data 
X = skin_segmentation.data.features
y = skin_segmentation.data.targets

# split the dataset into training (80%) and testing (20%)
np.random.seed(42)
indices = np.arange(X.shape[0])
np.random.shuffle(indices)

split = int(0.8*len(indices))
trainIndices = indices[:split]
testIndices = indices[split:]

X_train, X_test = X.iloc[trainIndices], X.iloc[testIndices]
y_train, y_test = y.iloc[trainIndices].values.ravel(), y.iloc[testIndices].values.ravel()

# implement Gaussian Naive Bayes
clf = GaussianNB()
clf.fit(X_train, y_train)

y_train_pred = clf.predict(X_train)
y_test_pred = clf.predict(X_test)

# Evaluation Metrics for NBC
def evaluate_model(y_true, y_pred, y_proba, dataset_name):
    """Evaluate and print metrics for a given dataset."""
    cfm = confusion_matrix(y_true, y_pred)
    sensitivity = cfm[1, 1] / (cfm[1, 1] + cfm[1, 0])
    specificity = cfm[0, 0] / (cfm[0, 0] + cfm[0, 1])

    print(f"\n{dataset_name} Metrics:")
    print("Confusion Matrix:\n", cfm)
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
    print(f"Sensitivity: {sensitivity:.4f}")
    print(f"Specificity: {specificity:.4f}")
    print(f"F1 Score: {f1_score(y_true, y_pred, average='binary'):.4f}")
    print(f"Log Loss: {log_loss(y_true, y_proba):.4f}")

evaluate_model(y_train, y_train_pred, clf.predict_proba(X_train), "Training")
evaluate_model(y_test, y_test_pred, clf.predict_proba(X_test), "Test")