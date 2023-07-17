# Import necessary libraries
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

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
    
    # Convert recommendations to Python list
    recommendations_list = recommendations.tolist()
    
    # Prepare response with recommendations, Age, FashionType, and OutfitChoice
    response = {
        'recommendations': recommendations_list,
        'age': age,
        'fashion_types': fashion_types,
        'outfit_choices': outfit_choices
    }
    
    return jsonify(response), 200

# Run the Flask application
if __name__ == '__main__':
    app.run()
