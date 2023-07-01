# main.py
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
import os.path

def preprocess_data(dataset):
    df = pd.DataFrame(dataset, columns=['age', 'gender', 'color', 'type'])

    # Convert gender and color to numerical values
    gender_encoder = LabelEncoder()
    if 'gender' in df.columns:
        df['gender'] = gender_encoder.fit_transform(df['gender'])

    color_encoder = LabelEncoder()
    if 'color' in df.columns:
        df['color'] = color_encoder.fit_transform(df['color'])

    # One-hot encode gender and color
    onehot_encoder = OneHotEncoder(sparse=False)
    if 'gender' in df.columns and 'color' in df.columns:
        encoded_features = onehot_encoder.fit_transform(df[['gender', 'color']])
    elif 'gender' in df.columns:
        encoded_features = onehot_encoder.fit_transform(df[['gender']])
    elif 'color' in df.columns:
        encoded_features = onehot_encoder.fit_transform(df[['color']])
    else:
        encoded_features = np.array([])

    # Normalize age using Min-Max scaling
    scaler = MinMaxScaler()
    if 'age' in df.columns:
        df['age'] = scaler.fit_transform(df[['age']])

    # Create preprocessed dataset with encoded and normalized features
    if len(encoded_features) > 0:
        preprocessed_data = pd.concat([df[['age']], pd.DataFrame(encoded_features)], axis=1)
    else:
        preprocessed_data = df[['age']]

    return preprocessed_data, gender_encoder, color_encoder, onehot_encoder, scaler

# Function to train and evaluate the model
def train_model(X_train, X_val, y_train, y_val):
    # Convert feature names to string types
    X_train.columns = X_train.columns.astype(str)
    X_val.columns = X_val.columns.astype(str)

    # Train a decision tree classifier
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = model.score(X_val, y_val)
    print("Model accuracy:", accuracy)

    return model

# Check if the CSV file exists
if os.path.isfile('user_input_data.csv'):
    # Load the existing data from the CSV file
    df = pd.read_csv('user_input_data.csv')
else:
    # Create a new DataFrame if the CSV file doesn't exist
    df = pd.DataFrame(columns=['age', 'gender', 'color', 'type'])

while True:
    # User input collection
    age = input("Enter your age: ")
    gender = input("Enter your gender (M/F): ")
    color = input("Enter your preferred clothing color: ")
    clothing_type = input("Enter the type of clothing you are looking for: ")

    # Store user input in the dataset
    user_data = {'age': age, 'gender': gender, 'color': color, 'type': clothing_type}

    # Append user input data to the existing DataFrame
    df = df.append(user_data, ignore_index=True)

    # Save the updated DataFrame to the CSV file
    df.to_csv('user_input_data.csv', index=False)

    # Preprocess the data
    preprocessed_data, gender_encoder, color_encoder, onehot_encoder, scaler = preprocess_data(df.values)

    # Train and evaluate the model
    if len(preprocessed_data) > 1:
        features = preprocessed_data.iloc[:, :-1]
        labels = preprocessed_data.iloc[:, -1]

        # Split the dataset into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(features, labels, test_size=0.2, random_state=42)

        # Train the model
        model = train_model(X_train, X_val, y_train, y_val)

        # Generate personalized recommendations
        age = scaler.transform([[float(age)]])
        gender_encoded = gender_encoder.transform([gender])
        color_encoded = color_encoder.transform([color])
        user_data_processed = np.concatenate([age[0], gender_encoded, color_encoded[0]])

        # Predict the desired clothing type
        predicted_label = model.predict([user_data_processed])

        # Generate recommendations based on the predicted label
        if predicted_label == 0:
            recommendations = ['T-shirt', 'Jeans']
        elif predicted_label == 1:
            recommendations = ['Dress', 'Skirt']
        else:
            recommendations = ['Shirt', 'Trousers']

        # Display the recommendations
        print("Recommended clothing:")
        for recommendation in recommendations:
            print(recommendation)
    else:
        print("Insufficient data for training the model.")

    choice = input("Do you want to continue? (Y/N): ")
    if choice.lower() != 'y':
        break
