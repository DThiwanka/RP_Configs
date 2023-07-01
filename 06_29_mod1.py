import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Load the data
data = pd.read_csv("./csvfiles/filemod2.csv")

# Create a user input form
user_id = st.text_input("Enter User ID", "1")
n_neighbors = st.slider("Select Number of Neighbors", 1, 10, 5)

if st.button("Get Recommendations"):
    try:
        # Convert user_id to int
        user_id = int(user_id)

        # Filter data for the given user_id
        user_data = data[data["UserId"] == user_id]

        # Drop unnecessary columns (if any)
        user_data = user_data.drop(columns=["UserId"])

        # Create X and y matrices
        X = data.drop(columns=["UserId"])
        y = data["UserId"]

        # Initialize Nearest Neighbors model
        nn = NearestNeighbors(n_neighbors=n_neighbors)
        nn.fit(X, y)

        # Find the nearest neighbors of the user
        _, indices = nn.kneighbors(user_data)

        # Get the recommendations from similar users
        similar_users = data.iloc[indices[0]]
        recommendations = similar_users["OutfitChoice"].value_counts().index.tolist()

        # Display recommendations
        st.success("Recommended Outfit Choices:")
        for recommendation in recommendations:
            st.write(recommendation)

    except ValueError:
        st.error("Invalid User ID. Please enter a valid integer.")
