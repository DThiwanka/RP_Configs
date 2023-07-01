# user_model.py

from sklearn.neighbors import NearestNeighbors
import numpy as np

def build_user_models(features):
    user_models = []

    for user_features in features:
        # Reshape user_features to match the expected shape for fitting the model
        user_features = np.reshape(user_features, (user_features.shape[0], -1))

        # Create a user model for each user
        model = NearestNeighbors(n_neighbors=5, metric='cosine')
        model.fit(user_features)
        user_models.append(model)

    return user_models

def generate_recommendations(user_input_features, user_models):
    recommendations = []

    # Use the user model to generate recommendations based on user input features
    for user_model in user_models:
        _, indices = user_model.kneighbors(user_input_features)
        recommendations.append(indices)

    return recommendations
