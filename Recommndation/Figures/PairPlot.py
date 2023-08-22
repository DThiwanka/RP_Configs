import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('../csvfiles/modified.csv')

# Get unique FashionType values
fashion_types = data['FashionType'].unique()

# Create a palette using the 'tab20' colormap
n_colors = len(fashion_types)
palette = sns.color_palette('tab20', n_colors=n_colors)

# Map each FashionType to a color
palette_dict = {fashion_type: color for fashion_type, color in zip(fashion_types, palette)}

# Create a pair plot
g = sns.pairplot(data, hue='FashionType', palette=palette_dict)

# Move the legend outside the plot
g.fig.subplots_adjust(right=0.85)  # Adjust the space for the legend
g.fig.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), title='FashionType')

plt.show()
