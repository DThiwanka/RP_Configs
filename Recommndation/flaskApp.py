import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import mode
import os
import threading
import time
import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# Download NLTK resources (uncomment these lines if you haven't downloaded them before)
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

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

# # Keep track of training history
# history = model.fit(X_encoded, y)
# training_history.append(history.history) # This line may vary based on the ML framework used


# Save the model to a file
model_file = './model/fashion_model.pkl'
joblib.dump(model, model_file)

# Initialize a list to store training history
training_history = []

# Function to calculate the mode of a list of values
def calculate_mode(values):
    freq_dist = {}
    for value in values:
        freq_dist[value] = freq_dist.get(value, 0) + 1
    max_freq = max(freq_dist.values())
    return [value for value, freq in freq_dist.items() if freq == max_freq]

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
    accuracy = model.score(X_encoded, y)
    training_history.append(accuracy)

    # Save the model to a file
    joblib.dump(model, model_file)

    print("Model trained successfully!")

# Function to calculate the most recommended age for a specific user
def get_most_recommended_age(user_id):
    user_data = data[data['UserID'] == user_id]
    outfit_choices = user_data['OutfitChoice'].tolist()

    similar_users = data[data['OutfitChoice'].isin(outfit_choices)]
    most_recommended_age = similar_users['Age'].mode().iloc[0]

    return int(most_recommended_age)

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
    
    # Get the most recommended age for the specific user
    most_recommended_age = get_most_recommended_age(int(user_id))

    # Tokenize the FashionType descriptions
    fashion_type_tokens = [word_tokenize(desc) for desc in fashion_types]
    
    # Flatten the list of tokens
    all_tokens = [token for sublist in fashion_type_tokens for token in sublist]
    
    # Calculate the frequency distribution of the tokens
    token_freq_dist = FreqDist(all_tokens)

    # Get the most common words in the FashionType descriptions
    most_common_words = token_freq_dist.most_common(3)

    # Convert recommendations to Python list
    recommendations_list = recommendations.tolist()
    
    # Prepare response with recommendations, Age, FashionType, OutfitChoice, and most recommended age
    response = {
        'recommendations': recommendations_list,
        'age': age,
        'fashion_types': fashion_types,
        'outfit_choices': outfit_choices,
        'most_recommended_age': most_recommended_age,
        'most_common_words': most_common_words
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

# Define API endpoint to get the current model status
@app.route('/model_status', methods=['GET'])
def get_model_status():
    global model

    model_status = "Trained" if model else "Not Trained"

    response = {
        'model_status': model_status
    }

    return jsonify(response), 200

# Define API endpoint to read more details from the model
@app.route('/model_details', methods=['GET'])
def get_model_details():
    global X
    global y
    global model

    # Get the feature names and target variable name
    feature_names = X.columns.tolist()
    target_variable = y.name

    # Get the number of data points used to train the model
    num_data_points = len(X)

    # Get the model's hyperparameters
    model_params = model.get_params()

    # Get the feature importances (if available, only applicable for certain models)
    feature_importances = None
    if hasattr(model, 'feature_importances_'):
        feature_importances = model.feature_importances_.tolist()

    # Get the accuracy of the model (if available, only applicable for classification models)
    accuracy = None
    if hasattr(model, 'score'):
        accuracy = model.score(X_encoded, y)

    # Get the model's classes (if available, only applicable for classification models)
    model_classes = None
    if hasattr(model, 'classes_'):
        model_classes = model.classes_.tolist()

    # Get the model's number of estimators (if available, only applicable for ensemble models)
    num_estimators = None
    if hasattr(model, 'n_estimators'):
        num_estimators = model.n_estimators

    # Get the model's criterion (if available, only applicable for certain models)
    criterion = None
    if hasattr(model, 'criterion'):
        criterion = model.criterion

    # Get the model's maximum depth (if available, only applicable for tree-based models)
    max_depth = None
    if hasattr(model, 'max_depth'):
        max_depth = model.max_depth

    # Get the model's training data shape
    data_shape = X.shape

    # Get the model's unique classes and their frequencies (if applicable, only for classification models)
    unique_classes_freq = None
    if hasattr(model, 'predict'):
        predictions = model.predict(X_encoded)
        unique_classes, class_counts = np.unique(predictions, return_counts=True)
        unique_classes_freq = dict(zip(unique_classes.tolist(), class_counts.tolist()))

    # Add any other relevant details about the model (you can add more as needed)
    # ...

    response = {
        'feature_names': feature_names,
        'target_variable': target_variable,
        'num_data_points': num_data_points,
        'data_shape': data_shape,
        'model_params': model_params,
        'feature_importances': feature_importances,
        'accuracy': accuracy,
        'model_classes': model_classes,
        'num_estimators': num_estimators,
        'criterion': criterion,
        'max_depth': max_depth,
        'unique_classes_freq': unique_classes_freq
        # Add more details here as needed
    }

    return jsonify(response), 200

# Define API endpoint to get the training history
@app.route('/get_training_history', methods=['GET'])
def get_training_history():
    global training_history

    if not training_history:
        return jsonify({'message': 'Model has not been trained yet. No training history available.'}), 404

    return jsonify({'training_history': training_history}), 200

# Run the Flask application
if __name__ == '__main__':
    app.run()

