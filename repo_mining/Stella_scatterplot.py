import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Generate data from previous file
inputfile = "data/file_rootbeer_authors_and_dates.csv"
data = pd.read_csv(inputfile)

# Sort the data by date
data['Date'] = pd.to_datetime(data['Date'])
dataSorted = data.sort_values(by='Date')
# Convert date to weeks 
dataSorted['Week'] = ((dataSorted['Date'] - dataSorted['Date'].min()).dt.days // 7)

# Add Index column for unique file index numbers
fileIdx = {file: idx + 1 for idx, file in enumerate(sorted(dataSorted['Filename'].unique()))}
dataSorted['Index'] = dataSorted['Filename'].map(fileIdx)

# create a scatterplot
authors = dataSorted['Author'].unique()
colors = plt.cm.tab20(np.linspace(0, 1, len(authors)))
author_color_map = {author: colors[i] for i, author in enumerate(authors)}

for author in authors:
    dataplot = dataSorted[dataSorted['Author'] == author]
    plt.scatter(dataplot['Index'], 
                dataplot['Week'], 
                s = 70,
                color=author_color_map[author], 
                label=author, 
                alpha=0.7
            )

plt.title("scottyab/rootbeer Repo")
plt.xlabel("File")
plt.ylabel("Weeks")
plt.legend(title="Author", bbox_to_anchor=(1.05, 1), loc='upper left')

# Output the scatterplot
plt.tight_layout()
fileOutput = 'data/file_rootbeer_scatterplot.png'
plt.savefig(fileOutput, dpi=200)
plt.show()