# Jaison-Noah Sarte - Lab 1 Git & Github
# CS 472 - Spring 2025
# Date: 1/26/2025

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import random

# Loading CSV of file name, author, and date
extractedData = pd.read_csv("data/data_rootbeer.csv")
# Converting Date into a datetime object
extractedData["Date"] = pd.to_datetime(extractedData["Date"])

# Calculate the number of weeks since the start of development
start_date = extractedData["Date"].min()
extractedData["Week"] = ((extractedData["Date"] - start_date).dt.days // 7)

# Getting singular files, no dupes of the same file
allFiles = np.unique(extractedData["File"])
# Indexing each file to have their own value
fileIndex = {}
for i in range(len(allFiles)):
    fileIndex[allFiles[i]] = i

# Replacing the file name with their value
extractedData["File"] = extractedData["File"].map(fileIndex) 

# Author Colors/Shades 
# Getting all the authors, no dupes
authors = np.unique(extractedData["Author"])
# Giving each author a random color
colorMap = {}

# For each author, generate a random color
for author in authors:
    # Hex format for color
    color = f"#{random.randint(0, 0xFFFFFF):06x}"
    # Assigning the color to the author
    colorMap[author] = color

# Converting to arrays
theWeeks = extractedData["Week"].to_numpy()
theFiles = extractedData["File"].to_numpy()
theAuthors = extractedData["Author"].to_numpy()

# Plotting
plt.figure(figsize=(14, 14))
for author in authors:
    # Creating mask for data of only the current author
    mask = (theAuthors == author)
    # Getting that authors touches each week
    theWeeksAuthor = theWeeks[mask]
    # Same for files
    theFilesAuthor = theFiles[mask]
    # Getting the color of the author
    theColor = colorMap[author]
    # Plotting the data
    plt.scatter(theFilesAuthor, theWeeksAuthor, c=theColor, alpha=0.5, edgecolor="black", label=author)

# Adding legend to display author names
plt.legend(title="Authors", bbox_to_anchor=(1.05, 1), loc='upper left')

# Labeling the plot
plt.title("Author File Touches by Week")
plt.xlabel("File Value")
plt.ylabel("Weeks")
y_ticks = np.arange(0, theWeeks.max() + 50, 50)  # Set y-axis ticks to go by 50's
plt.yticks(y_ticks) # Makes it more readable
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()