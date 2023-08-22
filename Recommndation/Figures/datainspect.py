import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv('../csvfiles/modified.csv')

# Display basic information about the dataset
print("Data Information:")
print(data.info())

# Display summary statistics
print("\nSummary Statistics:")
print(data.describe())

# Display the first few rows of the dataset
print("\nFirst Few Rows:")
print(data.head())

# Check for missing values
print("\nMissing Values:")
print(data.isnull().sum())

# Check unique values in categorical columns
print("\nUnique Values in Categorical Columns:")
categorical_columns = ['Gender', 'FashionType']
for col in categorical_columns:
    unique_values = data[col].unique()
    print(f"{col}: {unique_values}")

# Generate value counts for categorical columns
print("\nValue Counts for Categorical Columns:")
for col in categorical_columns:
    value_counts = data[col].value_counts()
    print(f"{col}:\n{value_counts}")

# Visualize the distribution of numerical columns
data[['Age', 'OutfitChoice']].hist(bins=20, figsize=(10, 6))
plt.suptitle('Distribution of Age and Outfit Choice')
plt.show()
