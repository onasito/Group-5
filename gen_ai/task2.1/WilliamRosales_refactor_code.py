import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

#Task 1
MnistData = pd.read_csv('MNIST_100.csv')
y = MnistData.iloc[:, 0]
x = MnistData.drop('label', axis=1)
print(x.shape)
print(y.shape)
pca = PCA(n_components=2)
pca.fit(x)
PCAX = pca.transform(x)
fig, T1 = plt.subplots()
# groups the data 0-9 in a scatter plot
for i in range(10):
    T1.scatter(PCAX[i*100:100+100*i, 0], PCAX[i*100:100+100*i, 1], label = i)
T1.legend()
plt.show()