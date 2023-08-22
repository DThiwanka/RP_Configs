import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the pickled model
with open('../model/fashion_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load your dataset
data = pd.read_csv('../csvfiles/modified.csv')

# Create a bar plot for FashionType distribution based on Gender
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='FashionType', hue='Gender', palette={'Male': 'blue', 'Female': 'pink'})
plt.xlabel('Fashion Type')
plt.ylabel('Count')
plt.title('Fashion Type Distribution based on Gender')
plt.legend(title='Gender')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
