import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier

# Load the CSV file
data = pd.read_csv("./csvfiles/file.csv")

# Split the data into features and target
X = data.drop(["FashionStyle"], axis=1)
y = data["FashionStyle"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the column transformer for one-hot encoding
preprocessor = ColumnTransformer(
    transformers=[("encoder", OneHotEncoder(), X.columns.tolist())],
    remainder="passthrough"
)

# Define the pipeline with the preprocessor and classifier
pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", MLPClassifier(max_iter=500))])


# Train the model
pipeline.fit(X_train, y_train)

# Streamlit GUI
st.title("Fashion Style Predictor")
st.write("Enter the details below to predict the fashion style.")

# Get unique values for each feature
age_values = data["Age"].unique()
gender_values = data["Gender"].unique()
fashion_type_values = data["FashionType"].unique()

# Create input fields in Streamlit
age = st.selectbox("Age", age_values)
gender = st.selectbox("Gender", gender_values)
fashion_type = st.selectbox("Fashion Type", fashion_type_values)

# Preprocess the user input
input_data = pd.DataFrame([[age, gender, fashion_type]], columns=["Age", "Gender", "FashionType"])

# Make prediction
prediction = pipeline.predict(input_data)
predicted_style = prediction[0]

st.write("Predicted Fashion Style:", predicted_style)
