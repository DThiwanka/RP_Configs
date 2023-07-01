import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder

# Train the k-nearest neighbors (k-NN) model
knn_model = NearestNeighbors(n_neighbors=3)

# Function to recommend fashion styles based on user input
def recommend_fashion(age, gender, fashion_type, k=3):
    # Define the fashion dataset
    fashion_data = {
        'Age': [25, 30, 35, 40, 45, 25, 30, 35, 40, 45],
        'Gender': ['Male', 'Male', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Female'],
        'FashionType': ['Casual', 'Formal', 'Casual', 'Formal', 'Casual', 'Formal', 'Casual', 'Formal', 'Casual', 'Formal'],
        'FashionStyle': ['Sporty', 'Classic', 'Bohemian', 'Minimalist', 'Vintage', 'Edgy', 'Preppy', 'Romantic', 'Streetwear', 'Glam']
    }

    # Preprocess the fashion data
    X = np.column_stack((fashion_data['Age'], fashion_data['Gender'], fashion_data['FashionType']))
    y = fashion_data['FashionStyle']

    # One-hot encode categorical features
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X)

    # Fit the k-NN model
    knn_model.fit(X_encoded)

    # Perform prediction for user input
    input_item = [age, gender, fashion_type]
    input_encoded = encoder.transform([input_item])
    distances, indices = knn_model.kneighbors(input_encoded)
    recommended_styles = []
    for index in indices.flatten():
        recommended_styles.append(y[index])
    return recommended_styles

# Get user input
age = int(input("Enter your age: "))
gender = input("Enter your gender (Male/Female): ")
fashion_type = input("Enter the desired fashion type: ")

# Generate recommendations based on user input
recommended_styles = recommend_fashion(age, gender, fashion_type)
if not recommended_styles:
    print("No matching fashion styles found. Please try different input.")
else:
    print("Recommended fashion styles:")
    for style in recommended_styles:
        print(style)
