import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from tensorflow import keras

# Load the fashion dataset
fashion_data = pd.DataFrame({
    'Age': [25, 30, 35, 40, 45, 25, 30, 35, 40, 45],
    'Gender': ['Male', 'Male', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Female'],
    'FashionType': ['Casual', 'Formal', 'Casual', 'Formal', 'Casual', 'Formal', 'Casual', 'Formal', 'Casual', 'Formal'],
    'FashionStyle': ['Sporty', 'Classic', 'Bohemian', 'Minimalist', 'Vintage', 'Edgy', 'Preppy', 'Romantic', 'Streetwear', 'Glam']
})

# Preprocess the fashion data
X = fashion_data[['Age', 'Gender', 'FashionType']]
y = fashion_data['FashionStyle']

# Encode categorical features using one-hot encoding
encoder = OneHotEncoder(sparse=False)
X_encoded = pd.DataFrame(encoder.fit_transform(X))
X_encoded.columns = encoder.get_feature_names_out(X.columns)

# Encode target labels using label encoding
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

# Create the neural network model
model = keras.models.Sequential()
model.add(keras.layers.Dense(64, activation='relu', input_dim=X_train.shape[1]))
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dense(len(np.unique(y_encoded)), activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=8, verbose=0)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print("Model accuracy:", accuracy)

# Function to recommend fashion styles based on user input
def recommend_fashion(age, gender, fashion_type):
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [gender],
        'FashionType': [fashion_type]
    })

    # Encode user input using one-hot encoding
    input_encoded = pd.DataFrame(encoder.transform(input_data))
    input_encoded.columns = encoder.get_feature_names_out(input_data.columns)

    # Make predictions
    predictions = model.predict(input_encoded)
    predicted_styles = np.argmax(predictions, axis=1)
    return label_encoder.inverse_transform(predicted_styles)

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
