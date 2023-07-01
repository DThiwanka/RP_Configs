import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Page 1: Input Data and Append to CSV

st.title("Fashion Recommendation System")

st.header("Page 1: Input Data")

age = st.number_input("Age")
gender = st.selectbox("Gender", ["Male", "Female"])
fashion_type = st.selectbox("Fashion Type", ["Casual", "Formal", "Sports"])
fashion_style = st.text_input("Fashion Style")

if st.button("Submit"):
    # Append the input data to the CSV file
    new_data = pd.DataFrame({"Age": [age],
                             "Gender": [gender],
                             "FashionType": [fashion_type],
                             "FashionStyle": [fashion_style]})
    new_data.to_csv("./csvfiles/filemod.csv", mode="a", header=False, index=False)
    st.success("Data appended to the CSV file.")

# Page 2: Recommendation System

st.header("Page 2: Recommendation System")

@st.cache(allow_output_mutation=True)  # Cache the function output to improve performance
def load_data():
    data = pd.read_csv("./csvfiles/filemod.csv")
    return data

data = load_data()

# Preprocess the data
X = data.drop(["OutfitChoice"], axis=1)
y = data["OutfitChoice"]

# Encode categorical features
X_encoded = pd.get_dummies(X, columns=["Gender", "FashionType", "FashionStyle"])

# Encode the target variable
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

# Train the classifier
classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)

# Make predictions
y_pred = classifier.predict(X_test)

# Convert encoded predictions back to original labels
y_pred_labels = encoder.inverse_transform(y_pred)

# Display the predictions
st.subheader("Predicted Outfit Choices")
st.table(pd.DataFrame({"Actual Outfit Choice": encoder.inverse_transform(y_test),
                       "Predicted Outfit Choice": y_pred_labels}))
