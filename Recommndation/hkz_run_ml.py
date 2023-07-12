import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Load the trained model
model = joblib.load("./model/fashion_model.pkl")

# Fashion Choices
fashion_choices = {
    "Casual Streetwear": [
        "Denim jeans, a graphic T-shirt, and sneakers",
        "Hoodie, leggings, and athletic shoes",
        "Distressed jeans, oversized hoodie, and sneakers"
    ],
    "Bohemian/Boho Chic": [
        "Flowy maxi dress and sandals",
        "Floral sundress and wedges",
        "Embroidered peasant top, flared jeans, and wedges"
    ],
    "Vintage-inspired": [
        "High-waisted pants, a blouse, and heels",
        "Polka dot swing dress, cat-eye sunglasses, and slingback heels",
        "Crochet top, flared pants, and platform sandals"
    ],
    "Minimalist": [
        "A-line skirt, tucked-in blouse, and ballet flats",
        "Cuffed chinos, a polo shirt, and loafers",
        "Flowy culottes, a structured top, and mules"
    ],
    "Preppy": [
        "Tailored blazer, trousers, and oxford shoes",
        "Plaid skirt, cashmere sweater, and pointed-toe flats",
        "Tailored jumpsuit, statement necklace, and stiletto pumps"
    ],
    "Edgy/Rock-inspired": [
        "Leather jacket, band T-shirt, ripped jeans, and ankle boots",
        "Plaid shirt, leather pants, combat boots, and spikes",
        "Leather biker jacket, striped tee, skinny jeans, and boots"
    ],
    "Athleisure": [
        "Athletic leggings, sports bra, and sneakers",
        "Track pants, hoodie, and trainers",
        "Sports shorts, tank top, and running shoes"
    ],
    "Glamorous": [
        "Sequin gown, statement earrings, and high heels",
        "Silk slip dress, faux fur coat, and strappy sandals",
        "Form-fitting cocktail dress, statement clutch, and stiletto heels"
    ]
    # Add more fashion types and outfit choices here
}

# Load the unique age values from the model
age_encoder = model["preprocessor"].named_transformers_["age_encoder"]
age_values = age_encoder.classes_

# Streamlit GUI
st.title("Fashion Style Predictor")
st.write("Enter the details below to predict the fashion style.")

# Get user input
user_id = st.text_input("User ID", "")
age = st.selectbox("Age", age_values)
gender = st.selectbox("Gender", ["Male", "Female"])
fashion_type = st.selectbox("Fashion Type", list(fashion_choices.keys()))

# Encode the user input
input_data = pd.DataFrame([[user_id, age, gender, fashion_type]], columns=["UserID", "Age", "Gender", "FashionType"])

# Make prediction
prediction = model.predict(input_data)
predicted_style = prediction[0]

st.write("Predicted Fashion Style:", predicted_style)

# Calculate cosine similarity between fashion styles
outfit_encodings = model["outfit_encodings"]
input_encoded = model["preprocessor"].transform(input_data.drop(["UserID"], axis=1))
cosine_sim = cosine_similarity(input_encoded, outfit_encodings)

# Find index of predicted style in the dataframe
predicted_style_index = list(fashion_choices.keys()).index(predicted_style)

# Get similar fashion styles based on cosine similarity
similar_styles_indices = cosine_sim[0].argsort()[::-1][1:4]
recommended_styles = [list(fashion_choices.keys())[i] for i in similar_styles_indices]

st.write("Recommended Fashion Styles:", recommended_styles)
