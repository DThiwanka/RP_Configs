import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Load the pickled model
with open('../model/fashion_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load your dataset
data = pd.read_csv('../csvfiles/modified.csv')

# Generate a scatter plot for Age vs FashionType
plt.figure(figsize=(10, 6))
plt.scatter(data['Age'], data['FashionType'], c=data['Gender'].map({'Male': 'blue', 'Female': 'pink'}))
plt.xlabel('Age')
plt.ylabel('Fashion Type')
plt.title('Age vs Fashion Type')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Male'),
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='pink', markersize=10, label='Female')])
plt.grid(True)
plt.show()
