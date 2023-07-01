# data_processing.py
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler
import pandas as pd

def preprocess_data(dataset):
    df = pd.DataFrame(dataset)

    # Convert gender and color to numerical values
    gender_encoder = LabelEncoder()
    df['gender'] = gender_encoder.fit_transform(df['gender'])

    color_encoder = LabelEncoder()
    df['color'] = color_encoder.fit_transform(df['color'])

    # One-hot encode gender and color
    onehot_encoder = OneHotEncoder(sparse=False)
    encoded_features = onehot_encoder.fit_transform(df[['gender', 'color']])

    # Normalize age using Min-Max scaling
    scaler = MinMaxScaler()
    df['age'] = scaler.fit_transform(df[['age']])

    # Create preprocessed dataset with encoded and normalized features
    preprocessed_data = pd.concat([df[['age']], pd.DataFrame(encoded_features)], axis=1)

    return preprocessed_data, gender_encoder, onehot_encoder, scaler
