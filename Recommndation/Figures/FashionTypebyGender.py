import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('../csvfiles/modified.csv')

# Create a box plot of FashionType by Gender
plt.figure(figsize=(10, 6))
sns.boxplot(data=data, x='FashionType', y='OutfitChoice', hue='Gender', palette='Set3')
plt.xlabel('Fashion Type')
plt.ylabel('Outfit Choice')
plt.title('Fashion Type by Gender')
plt.legend(title='Gender')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
