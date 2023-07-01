import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity

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

# Calculate cosine similarity between fashion styles
outfit_encodings = ct.transform(data)
cosine_sim = cosine_similarity(outfit_encodings)

# Find index of predicted style in the dataframe
predicted_style_index = data[data["OutfitChoice"] == predicted_style].index[0]

# Get similar fashion styles based on cosine similarity
similar_styles_indices = cosine_sim[predicted_style_index].argsort()[::-1][1:4]
recommended_styles = data.loc[similar_styles_indices, "OutfitChoice"].tolist()

st.write("Recommended Fashion Styles:", recommended_styles)
