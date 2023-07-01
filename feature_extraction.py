# feature_extraction.py

import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input

def extract_features(images):
    model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, pooling='avg')

    # Preprocess the images for the ResNet50 model
    preprocessed_images = []
    for image in images:
        preprocessed_image = preprocess_input(image)
        preprocessed_images.append(preprocessed_image)

    # Convert the list to numpy array
    preprocessed_images = tf.stack(preprocessed_images)

    # Extract features using the ResNet50 model
    features = model.predict(preprocessed_images)

    return features
