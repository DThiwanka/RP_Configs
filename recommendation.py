# recommendation.py
import numpy as np

def generate_recommendations(model, user_data, label_encoder, onehot_encoder, scaler):
    # Preprocess the user data
    age = user_data['age']
    gender = user_data['gender']
    color = user_data['color']

    # Encode gender and color
    gender_encoded = label_encoder.transform([gender])
    color_encoded = label_encoder.transform([color])

    # One-hot encode gender and color
    encoded_gender = onehot_encoder.transform([[gender_encoded[0]]])
    encoded_color = onehot_encoder.transform([[color_encoded[0]]])

    # Normalize age
    normalized_age = scaler.transform([[age]])

    # Combine all features
    user_data_processed = np.concatenate([normalized_age, encoded_gender.flatten(), encoded_color.flatten()])

    # Predict the desired clothing type
    predicted_label = model.predict([user_data_processed])

    # Generate recommendations based on the predicted label
    recommendations = get_recommendations(predicted_label, label_encoder)

    return recommendations

def get_recommendations(label, label_encoder):
    # Placeholder function to generate recommendations based on label
    # You can replace this with your own logic or connect to a fashion database/API
    if label == 0:
        return ['T-shirt', 'Jeans']
    elif label == 1:
        return ['Dress', 'Skirt']
    else:
        return ['Shirt', 'Trousers']
