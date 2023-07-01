import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load the CSV file
data = pd.read_csv("./csvfiles/filemod2.csv")

# Perform label encoding on the target variable
encoder = LabelEncoder()
data["OutfitChoiceEncoded"] = encoder.fit_transform(data["OutfitChoice"])

# Split the data into features and target
X = data.drop(["OutfitChoiceEncoded"], axis=1)
y = data["OutfitChoiceEncoded"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Perform label encoding on categorical columns
categorical_columns = ['UserId', 'Age', 'Gender']
for col in categorical_columns:
    encoder = LabelEncoder()
    X_train[col] = encoder.fit_transform(X_train[col])
    X_test[col] = encoder.transform(X_test[col])

# Print unique values of the FashionType column
unique_fashion_types = X_train["FashionType"].unique()
st.write("Unique Fashion Types:", unique_fashion_types)
