import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from surprise import Dataset, Reader, SVD

# Load the CSV file
data = pd.read_csv("./csvfiles/filemod2.csv")

# Perform label encoding on the target variable
encoder = LabelEncoder()
data["OutfitChoiceEncoded"] = encoder.fit_transform(data["OutfitChoice"])

# Split the data into features and target
X = data.drop(["OutfitChoice"], axis=1)
y = data["OutfitChoiceEncoded"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the column transformer for one-hot encoding
ct = ColumnTransformer(
    transformers=[("encoder", OneHotEncoder(handle_unknown='ignore'), ["UserId", "Age", "Gender", "FashionType"])],
    remainder="passthrough"
)

# Apply the column transformer on the input features
X_train_encoded = ct.fit_transform(X_train)
X_test_encoded = ct.transform(X_test)

# Create a random forest classifier
classifier = RandomForestClassifier()

# Train the classifier
classifier.fit(X_train_encoded, y_train)

# Streamlit GUI
st.title("Fashion Style Predictor")
st.write("Enter the details below to predict the fashion style.")

# Get user input
user_id = st.text_input("User ID", "")
age = st.selectbox("Age", data["Age"].unique())
gender = st.selectbox("Gender", data["Gender"].unique())
fashion_type = st.selectbox("Fashion Type", data["FashionType"].unique())

# Encode the user input
input_data = pd.DataFrame([[user_id, age, gender, fashion_type]], columns=["UserId", "Age", "Gender", "FashionType"])
input_data["OutfitChoiceEncoded"] = 0  # Placeholder value, not used in prediction
input_encoded = ct.transform(input_data)

# Make prediction
prediction = classifier.predict(input_encoded)
predicted_style = encoder.inverse_transform(prediction)[0]

st.write("Predicted Fashion Style:", predicted_style)

# Prepare data for recommendation
reader = Reader(rating_scale=(0, len(encoder.classes_) - 1))
dataset = Dataset.load_from_df(data[['UserId', 'FashionType', 'OutfitChoiceEncoded']], reader)

# Build the recommendation model using SVD
trainset = dataset.build_full_trainset()
algo = SVD()
algo.fit(trainset)

# Get fashion style recommendations based on user ID and inputs
if user_id:
    user_choices = data[data["UserId"] == user_id]["OutfitChoiceEncoded"].unique()
    predictions = []
    for choice in user_choices:
        prediction = algo.predict(user_id, choice)
        predictions.append((encoder.inverse_transform([choice])[0], prediction.est))
    predictions.sort(key=lambda x: x[1], reverse=True)
    recommended_styles = [choice for choice, _ in predictions[:3]]
    st.write("Recommended Fashion Styles:", recommended_styles)
