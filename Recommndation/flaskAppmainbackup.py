# Import necessary libraries
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import mode
import os
import threading
import time
import joblib

# Load the CSV file
data = pd.read_csv('./csvfiles/fashion_data_forHkz_run.csv')

# Data preprocessing
# Drop any rows with missing values
data.dropna(inplace=True)

# Split features and target variable
X = data.drop(['OutfitChoice'], axis=1)
y = data['OutfitChoice']

# Perform one-hot encoding on categorical features
encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(X.drop('UserID', axis=1)).toarray()

# Train the RandomForestClassifier model
model = RandomForestClassifier()
model.fit(X_encoded, y)

# Save the model to a file
model_file = './model/fashion_model.pkl'
joblib.dump(model, model_file)

# Function to train the model
def train_model():
    global model
    global data

    # Load the CSV file
    data = pd.read_csv('./csvfiles/fashion_data_forHkz_run.csv')

    # Data preprocessing
    # Drop any rows with missing values
    data.dropna(inplace=True)

    # Split features and target variable
    X = data.drop(['OutfitChoice'], axis=1)
    y = data['OutfitChoice']

    # Perform one-hot encoding on categorical features
    encoder = OneHotEncoder()
    X_encoded = encoder.fit_transform(X.drop('UserID', axis=1)).toarray()

    # Train the RandomForestClassifier model
    model = RandomForestClassifier()
    model.fit(X_encoded, y)

    # Save the model to a file
    joblib.dump(model, model_file)

    print("Model trained successfully!")


# Function to check for CSV changes and trigger model training
def check_csv_changes():
    global data

    # Get the initial timestamp of the CSV file
    initial_timestamp = os.path.getmtime('./csvfiles/fashion_data_forHkz_run.csv')

    while True:
        # Sleep for 1 second to avoid continuous checks
        time.sleep(1)

        # Get the current timestamp of the CSV file
        current_timestamp = os.path.getmtime('./csvfiles/fashion_data_forHkz_run.csv')

        # Check if the CSV file has been modified
        if current_timestamp != initial_timestamp:
            print("Detected changes in the CSV file. Retraining the model...")
            train_model()

            # Update the initial timestamp with the current timestamp
            initial_timestamp = current_timestamp

# Start a separate thread to check for CSV changes and trigger model training
csv_thread = threading.Thread(target=check_csv_changes)
csv_thread.start()

# Create Flask application
app = Flask(__name__)

# Define API endpoint
@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    user_id = request.json['user_id']
    
    # Check if the user ID exists in the CSV data
    if int(user_id) not in data['UserID'].values:
        return jsonify({'error': 'Invalid User ID. Please enter a valid User ID.'}), 400
    
    # Find the user's past bought items
    user_data = data[data['UserID'] == int(user_id)]
    user_features = user_data.drop(['UserID', 'OutfitChoice'], axis=1)
    
    # Perform one-hot encoding on user features
    user_encoded = encoder.transform(user_features).toarray()
    
    # Get recommendations
    recommendations = model.predict(user_encoded)
    
    # Retrieve Age, FashionType, and OutfitChoice for user's past bought items
    age = user_data['Age'].tolist()
    fashion_types = user_data['FashionType'].tolist()
    outfit_choices = user_data['OutfitChoice'].tolist()
    
    # Get the most common/recommended age among users with similar outfit choices
    similar_users = data[data['OutfitChoice'].isin(outfit_choices)]
    most_recommended_age = mode(similar_users['Age'], keepdims=True)[0][0]

    
    # Convert recommendations to Python list
    recommendations_list = recommendations.tolist()
    
    # Prepare response with recommendations, Age, FashionType, OutfitChoice, and most recommended age
    response = {
        'recommendations': recommendations_list,
        'age': age,
        'fashion_types': fashion_types,
        'outfit_choices': outfit_choices,
        'most_recommended_age': int(most_recommended_age)
    }
    
    return jsonify(response), 200


# Define API endpoint to insert data
@app.route('/insert_data', methods=['POST'])
def insert_data():
    try:
        # Indicate 'data' as a global variable
        global data
        
        new_data = request.get_json()

        # Convert the new data to a dictionary
        new_data_dict = {
            'UserID': [new_data['UserID']],
            'Age': [new_data['Age']],
            'Gender': [new_data['Gender']],
            'FashionType': [new_data['FashionType']],
            'OutfitChoice': [new_data['OutfitChoice']]
        }

        # Create a DataFrame from the new data with a specified index
        new_data_df = pd.DataFrame(new_data_dict)

        # Append the new data DataFrame to the original data DataFrame
        data = data.append(new_data_df, ignore_index=True)

        # Perform any necessary data preprocessing

        # Save the updated DataFrame to the CSV file
        data.to_csv('./csvfiles/fashion_data_forHkz_run.csv', index=False)

        return jsonify({'message': 'Data inserted successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Define API endpoint for training the model
@app.route('/train_model', methods=['POST'])
def trigger_training():
    try:
        train_model()
        return jsonify({'message': 'Model trained successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#############################################################
@app.route('/get_recommendations', methods=['POST'])
def get_user_recommendations():
    user_id = request.json['user_id']
    
    # Check if the user ID exists in the CSV data
    if int(user_id) not in data['UserID'].values:
        return jsonify({'error': 'Invalid User ID. Please enter a valid User ID.'}), 400
    
    # Find the user's past bought items
    user_data = data[data['UserID'] == int(user_id)]
    user_features = user_data.drop(['UserID', 'OutfitChoice'], axis=1)
    
    # Perform one-hot encoding on user features
    user_encoded = encoder.transform(user_features).toarray()
    
    # Get predictions for user's past bought items
    predictions = model.predict(user_encoded)
    
    # Retrieve most recommended FashionTypes and OutfitChoices
    fashion_type_counts = user_data['FashionType'].value_counts()
    most_recommended_fashion_types = fashion_type_counts.nlargest(3).index.tolist()
    
    outfit_choice_counts = user_data['OutfitChoice'].value_counts()
    most_recommended_outfit_choices = outfit_choice_counts.nlargest(3).index.tolist()
    
    # Prepare response with most recommended FashionTypes and OutfitChoices
    response = {
        'most_recommended_fashion_types': most_recommended_fashion_types,
        'most_recommended_outfit_choices': most_recommended_outfit_choices
    }
    
    return jsonify(response), 200

#############################################################

# Run the Flask application
if __name__ == '__main__':
    app.run()