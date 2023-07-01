import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier

# Load the CSV file
data = pd.read_csv("./csvfiles/filemod.csv")

# Split the data into features and target
X = data.drop(["OutfitChoice"], axis=1)
y = data["OutfitChoice"]

# Perform label encoding on the target variable
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Define the column transformer for one-hot encoding
ct = ColumnTransformer(
    transformers=[("encoder", OneHotEncoder(handle_unknown='ignore'), ["Age", "Gender", "FashionType"])],
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
age = st.selectbox("Age", data["Age"].unique())
gender = st.selectbox("Gender", data["Gender"].unique())
fashion_type = st.selectbox("Fashion Type", data["FashionType"].unique())

# Encode the user input
input_data = pd.DataFrame([[age, gender, fashion_type]], columns=["Age", "Gender", "FashionType"])
input_encoded = ct.transform(input_data)

# Make prediction
prediction = classifier.predict(input_encoded)
predicted_style = encoder.inverse_transform(prediction)[0]

st.write("Predicted Fashion Style:", predicted_style)

# # Get predictions for all data
# all_predictions = classifier.predict(ct.transform(X))
# data["PredictedStyle"] = encoder.inverse_transform(all_predictions)

# # Show all predictions
# st.write("All Predictions:")
# st.write(data)
