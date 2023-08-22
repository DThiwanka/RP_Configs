import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('../csvfiles/modified.csv')

# Plot a bar plot for Gender distribution
plt.figure(figsize=(8, 6))
sns.countplot(data=data, x='Gender')
plt.title('Gender Distribution')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.show()

# Plot a bar plot for FashionType distribution
plt.figure(figsize=(12, 6))
sns.countplot(data=data, y='FashionType', order=data['FashionType'].value_counts().index)
plt.title('FashionType Distribution')
plt.xlabel('Count')
plt.ylabel('FashionType')
plt.show()

# Plot a pie chart for OutfitChoice distribution
plt.figure(figsize=(8, 8))
outfit_counts = data['OutfitChoice'].value_counts()
plt.pie(outfit_counts, labels=outfit_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('OutfitChoice Distribution')
plt.show()

# Plot a bar plot for Gender and FashionType
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='Gender', hue='FashionType')
plt.title('Gender Distribution by FashionType')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.legend(title='FashionType')
plt.show()

# Plot a stacked bar plot for Gender and FashionType
plt.figure(figsize=(10, 6))
data_gender_fashion = data.groupby(['Gender', 'FashionType']).size().unstack()
data_gender_fashion.plot(kind='bar', stacked=True)
plt.title('Stacked Gender Distribution by FashionType')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.legend(title='FashionType')
plt.show()
