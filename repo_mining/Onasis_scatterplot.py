import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("file_data.csv")

# Convert the Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Get the minimum date to use as a reference for week calculation
min_date = df["Date"].min()
df["Week"] = ((df["Date"] - min_date).dt.days // 7)

# Assign unique numbers to each file
file_mapping = {file: idx + 1 for idx, file in enumerate(df["Filename"].unique())}  # Start numbering from 1
df["FileNumber"] = df["Filename"].map(file_mapping)

# Print the file mapping for reference
print("Filename to Number Mapping:")
for filename, number in file_mapping.items():
    print(f"{number}: {filename}")

# Create a color map for each author
authors = df["Author"].unique()
cmap = plt.get_cmap("tab20")
colors = {author: cmap(i / len(authors)) for i, author in enumerate(authors)}

# Plot scatter plot
plt.figure(figsize=(12, 6))

for author in authors:
    author_df = df[df["Author"] == author]
    plt.scatter(author_df["FileNumber"], author_df["Week"], color=colors[author], label=author, alpha=0.6)

# Labeling
plt.xlabel("File Number")
plt.ylabel("Weeks Since First Entry")
plt.title("Scatter Plot of File Changes Over Time")
plt.xticks(ticks=list(file_mapping.values()), labels=list(file_mapping.values()), rotation=90, fontsize=8)

plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(title="Author")

plt.tight_layout()
plt.show()