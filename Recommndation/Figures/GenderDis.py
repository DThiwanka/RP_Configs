import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('../csvfiles/modified.csv')

# Create a bar plot of Gender distribution
plt.figure(figsize=(8, 6))
sns.countplot(data=data, x='Gender', palette='Set2')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.title('Gender Distribution')
plt.show()
