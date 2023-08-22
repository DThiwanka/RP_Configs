import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('../csvfiles/modified.csv')

# Plot a count plot for Gender and OutfitChoice
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='Gender', hue='OutfitChoice')
plt.title('Gender Distribution by OutfitChoice')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.legend(title='OutfitChoice')
plt.show()

# Clean 'Age' column and convert 'FashionType' to categorical
data['Age'] = pd.to_numeric(data['Age'], errors='coerce')
data['FashionType'] = pd.Categorical(data['FashionType'])

# Plot a bar plot for average Age by FashionType
plt.figure(figsize=(12, 6))
sns.barplot(data=data, y='FashionType', x='Age')
plt.title('Average Age by FashionType')
plt.xlabel('Average Age')
plt.ylabel('FashionType')
plt.show()

# Clean 'Age' column and convert 'FashionType' to categorical
data['Age'] = pd.to_numeric(data['Age'], errors='coerce')
data['FashionType'] = pd.Categorical(data['FashionType'])

# Plot a violin plot for Age distribution by Gender
plt.figure(figsize=(10, 6))
sns.violinplot(data=data, x='Gender', y='Age')
plt.title('Age Distribution by Gender')
plt.xlabel('Gender')
plt.ylabel('Age')
plt.show()
# Plot a swarm plot for FashionType and Age
plt.figure(figsize=(12, 6))
sns.swarmplot(data=data, x='FashionType', y='Age')
plt.title('Age Distribution by FashionType')
plt.xlabel('FashionType')
plt.ylabel('Age')
plt.show()

# Plot a box plot for Age distribution by OutfitChoice
plt.figure(figsize=(10, 6))
sns.boxplot(data=data, x='OutfitChoice', y='Age')
plt.title('Age Distribution by OutfitChoice')
plt.xlabel('OutfitChoice')
plt.ylabel('Age')
plt.show()
