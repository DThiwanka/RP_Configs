import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('../csvfiles/modified.csv')

# Create a histogram of Age
plt.figure(figsize=(10, 6))
plt.hist(data['Age'], bins=20, edgecolor='k')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Histogram of Age')
plt.grid(True)
plt.show()
