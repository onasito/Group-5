# Import libraries
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns # for custom colors
import colorcet as cc # for custom colors

# Read the file into a dataframe 
authorsDates = pd.read_csv('data/file_authorDate.csv')
# print(authorsDates.head())

# Sort the dataframe by date 
authorsDates['Date'] = pd.to_datetime(authorsDates['Date'])
authDateSorted = authorsDates.sort_values(by='Date')
# print(authDateSorted.head())

# Assign weeks variable 
authDateWeeks = authDateSorted
earliestDate = authDateWeeks['Date'].min() 
# print(earliestDate)
authDateWeeks['Weeks'] = ((authDateWeeks['Date'] - earliestDate).dt.days // 7)

# Get unique x-values
uniqueFiles = authDateWeeks['Filename'].unique()  
# Use a dictionary to assign unique file names with unique numbers 
fileNums = dict()
i = 1
for file in uniqueFiles: 
    fileNums[file] = i
    i=i+1
# Create new dataframe
authDateWksNums = authDateWeeks
# Create new column for file number
authDateWksNums['FileNum'] = None
# Assign file number stored in dictionary
for index, row in authDateWksNums.iterrows():
    fname = row['Filename']
    authDateWksNums.at[index,'FileNum'] = fileNums[fname]

# Create scatter plot 
plt.figure(figsize=(10, 6))
custom_palette = sns.color_palette(cc.glasbey_light, n_colors=24)
sns.scatterplot(data=authDateWksNums, x='FileNum', y='Weeks', hue='Author', palette=custom_palette, s=25)
plt.xlabel('File')
plt.ylabel('Weeks')
plt.title('Commit History for scottyab/rootbeer Repo')
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), title='Authors')
plt.tight_layout()
plt.savefig('data/image_plot.png', dpi=300)