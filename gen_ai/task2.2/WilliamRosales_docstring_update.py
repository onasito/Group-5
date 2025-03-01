import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#read in the data from cvs files
trainingData = pd.read_csv('MNIST_training.csv')
testData = pd.read_csv('MNIST_test.csv')
y = trainingData.iloc[:,0]
x = trainingData.drop('label', axis=1)

SampleData = np.array(x.iloc[:], dtype=float)

y2= testData.iloc[:,0]

ground_Truth = np.array(np.transpose(y2.values))
x2 = testData.drop('label', axis=1)

#will obtain the distance id the data
#SampleData[01...ij] - Test Sample[0....ith] = newMatrix[]
#Sum(newMatrix^2) and sqr(sum)
guessList= []
a = len(SampleData)

#k
for k in range (1, 20, 2):
    correct = 0
    wrong = 0
    for i in range(0, 50, 1):
        TestD = x2.iloc[i,:]
        Testi = np.array(TestD, dtype=float)
        testi = np.tile(Testi, (a,1))
        tmpMatrix = np.sum(np.square(SampleData - testi), axis=1)
        tmpDistance = np.sqrt(tmpMatrix)
        kneighbors = y[np.argsort(tmpDistance)[:k]]
        tmp = np.bincount(kneighbors)
        guess = np.argmax(tmp)
        if guess == y2[i]:
            correct = correct + 1
        else:
            wrong = wrong + 1
    print("K value : ", k)
    print("correctly classified : ", correct, "incorrectly classified : ", wrong)
    print("Accuracy : ", correct/len(y2),"\n")
