import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('../csvfiles/modified.csv')

# Create a scatter plot of Age vs OutfitChoice
plt.figure(figsize=(10, 6))
plt.scatter(data['Age'], data['OutfitChoice'], alpha=0.5)
plt.xlabel('Age')
plt.ylabel('Outfit Choice')
plt.title('Age vs Outfit Choice')
plt.grid(True)
plt.show()
