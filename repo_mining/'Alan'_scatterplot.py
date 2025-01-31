import csv
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

# Load the authors and dates data from the CSV file
input_file = 'data/authors_dates_rootbeer.csv'  # Replace 'rootbeer' with your repo name if needed

data = []

with open(input_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        filename, author, date = row
        try:
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')  # Convert ISO date to datetime
            data.append((filename, author, date))
        except ValueError as e:
            print(f"Error parsing date: {e}")

# Convert to a pandas DataFrame
df = pd.DataFrame(data, columns=['Filename', 'Author', 'Date'])

# Extract the week number from the dates using the ISO calendar
df['Week'] = df['Date'].dt.isocalendar().week

# Count the number of touches per file and per week
df_summary = df.groupby(['Filename', 'Author', 'Week']).size().reset_index(name='Touches')

# Map filenames to unique indices
df_summary['FileIndex'] = df_summary['Filename'].astype('category').cat.codes

# Create a scatter plot
plt.figure(figsize=(14, 8))

# Map authors to unique colors
authors = df_summary['Author'].unique()
colors = plt.cm.get_cmap('tab10', len(authors))
color_map = {author: colors(i) for i, author in enumerate(authors)}

# Plot each data point
for author in authors:
    author_data = df_summary[df_summary['Author'] == author]
    plt.scatter(
        author_data['FileIndex'],
        author_data['Week'],
        s=author_data['Touches'] * 20,
        color=color_map[author],
        label=author,
        alpha=0.7
    )

# Set plot title and labels
plt.title('Scatter Plot of Weeks vs File Touches by Author', fontsize=16)
plt.xlabel('File Index', fontsize=12)
plt.ylabel('Weeks', fontsize=12)

# Adjust x-axis ticks for file indices
plt.xticks(range(len(df_summary['FileIndex'].unique())), range(len(df_summary['FileIndex'].unique())), rotation=90, fontsize=8)

# Adjust y-axis ticks for weeks
plt.yticks(range(0, 53, 5), range(0, 53, 5))

# Add legend and grid
plt.legend(title='Author', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(visible=True, linestyle='--', alpha=0.5)

# Save the scatter plot
output_file = 'data/scatterplot_weeks_vs_files.png'
plt.tight_layout()
plt.savefig(output_file)

print(f"Scatter plot has been saved to {output_file}.")
plt.show()
