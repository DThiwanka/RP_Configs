import os
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

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

# CSV file path
csv_file = "./csvfiles/fashion_data_forHkz_run.csv"
model_file = "./model/fashion_model.pkl"


# Function to append data to CSV file
def append_data_to_csv(data):
    if not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0:
        pd.DataFrame([data]).to_csv(csv_file, index=False)
    else:
        df = pd.read_csv(csv_file)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(csv_file, index=False)


def preprocess_data(df):
    # Encode categorical variables
    label_encoder = LabelEncoder()
    df["Gender"] = label_encoder.fit_transform(df["Gender"])
    df["FashionType"] = label_encoder.fit_transform(df["FashionType"])

    # Perform feature encoding (one-hot encoding)
    categorical_features = ["Gender", "FashionType"]
    encoded_features = pd.get_dummies(df[categorical_features], columns=categorical_features)
    df = pd.concat([df.drop(categorical_features, axis=1), encoded_features], axis=1)

    # Perform feature selection
    X = df.drop("OutfitChoice", axis=1)
    y = df["OutfitChoice"]

    # Perform feature transformation (e.g., scaling)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Apply feature selection on scaled features
    selector = SelectKBest(score_func=f_classif, k=2)
    X_selected = selector.fit_transform(X_scaled, y)

    # Get selected feature names
    selected_features_indices = selector.get_support(indices=True)
    selected_features = X.columns[selected_features_indices].tolist()

    # Create new DataFrame with selected features and target variable
    df_selected = pd.DataFrame(X_selected, columns=selected_features)
    df_selected["OutfitChoice"] = y

    return df_selected


def train_model(df):
    # Split the data into features (X) and target (y)
    X = df.drop("OutfitChoice", axis=1)
    y = df["OutfitChoice"]

    # Train the model (using Random Forest as an example)
    model = RandomForestClassifier()
    model.fit(X, y)

    return model


def save_model(model):
    joblib.dump(model, model_file)


def load_model():
    return joblib.load(model_file)


def main():
    st.title("Fashion Outfit Selector")

    # User inputs
    user_id = st.text_input("User ID")
    age = st.text_input("Age")
    gender = st.selectbox("Gender", ["Male", "Female"])

    # Fashion Type selection
    fashion_type = st.selectbox("Select Fashion Type", list(fashion_choices.keys()))

    # Outfit Choices based on selected Fashion Type
    if fashion_type:
        outfit_choices = fashion_choices[fashion_type]
        outfit_choice = st.selectbox("Select Outfit Choice", outfit_choices)

        # Save Outfit button
        if st.button("Save Outfit"):
            data = {
                "UserID": user_id,
                "Age": age,
                "Gender": gender,
                "FashionType": fashion_type,
                "OutfitChoice": outfit_choice
            }
            append_data_to_csv(data)
            st.success("Outfit saved successfully!")

    # Train the model with saved data
    if st.button("Train Model"):
        df = pd.read_csv(csv_file)
        df = preprocess_data(df)
        model = train_model(df)
        save_model(model)
        st.success("Model trained and saved successfully!")


if __name__ == "__main__":
    main()
