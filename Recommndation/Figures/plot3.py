import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('../csvfiles/modified.csv')

# Clean 'Age' column and convert 'FashionType' to categorical
data['Age'] = pd.to_numeric(data['Age'], errors='coerce')
data['FashionType'] = pd.Categorical(data['FashionType'])

# Rename 'Edgy/Rock-inspired' category temporarily
data['FashionType'] = data['FashionType'].replace('Edgy/Rock-inspired', 'Edgy_Rock_inspired')

# Plot a pair plot for Age, Gender, and FashionType
sns.pairplot(data, hue='Gender', palette={'Male': 'blue', 'Female': 'pink'})
plt.title('Pair Plot of Age, Gender, and FashionType')
plt.show()

# Restore the original category name
data['FashionType'] = data['FashionType'].replace('Edgy_Rock_inspired', 'Edgy/Rock-inspired')
