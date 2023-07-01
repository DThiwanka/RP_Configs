from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Function to load or create a CSV file
def load_csv(filename):
    try:
        data = pd.read_csv(filename)
    except FileNotFoundError:
        data = pd.DataFrame(columns=["Age", "Gender", "FashionType", "FashionStyle", "OutfitChoice"])
    return data

# Function to save data to a CSV file
def save_csv(data, filename):
    data.to_csv(filename, index=False)

# Function to preprocess data and train the model
def preprocess_and_train(data):
    # Split the data into features and target
    X = data.drop(["OutfitChoice"], axis=1)
    y = data["OutfitChoice"]

    # Perform label encoding on the target variable
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    # Define the column transformer for one-hot encoding
    ct = ColumnTransformer(
        transformers=[("encoder", OneHotEncoder(handle_unknown='ignore'), ["Age", "Gender", "FashionType", "FashionStyle"])],
        remainder="passthrough"
    )

    # Apply the column transformer on the input features
    X_encoded = ct.fit_transform(X)

    # Create a random forest classifier
    classifier = RandomForestClassifier()

    # Train the classifier
    classifier.fit(X_encoded, y_encoded)

    return classifier, encoder, ct

# Function to get fashion style recommendation
def get_recommendation(input_data, classifier, encoder, ct):
    # Encode the user input
    input_encoded = ct.transform(input_data)

    # Make prediction
    prediction = classifier.predict(input_encoded)
    predicted_style = encoder.inverse_transform(prediction)[0]

    return predicted_style

# Home page
@app.route("/")
def home():
    return render_template("./index.html")

# Input Data page
@app.route("/input_data", methods=["GET", "POST"])
def input_data():
    if request.method == "POST":
        # Load or create the CSV file
        data = load_csv("fashion_data.csv")

        # Get user input
        age = request.form["age"]
        gender = request.form["gender"]
        fashion_type = request.form["fashion_type"]
        fashion_style = request.form["fashion_style"]
        outfit_choice = request.form["outfit_choice"]

        # Add data to the CSV file
        new_data = pd.DataFrame([[age, gender, fashion_type, fashion_style, outfit_choice]], columns=["Age", "Gender", "FashionType", "FashionStyle", "OutfitChoice"])
        data = data.append(new_data, ignore_index=True)
        save_csv(data, "fashion_data.csv")

        return render_template("input_data.html", message="Data added successfully!")

    return render_template("input_data.html", message="")

# Recommendation page
@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    # Load the CSV file
    data = load_csv("fashion_data.csv")

    if data.empty:
        return render_template("recommendation.html", message="No data available. Please add data using the 'Input Data' page.")

    if request.method == "POST":
        # Preprocess data and train the model
        classifier, encoder, ct = preprocess_and_train(data)

        # Get user input
        age = request.form["age"]
        gender = request.form["gender"]
        fashion_type = request.form["fashion_type"]
        fashion_style = request.form["fashion_style"]

        # Encode the user input
        input_data = pd.DataFrame([[age, gender, fashion_type, fashion_style]], columns=["Age", "Gender", "FashionType", "FashionStyle"])

        # Get fashion style recommendation
        predicted_style = get_recommendation(input_data, classifier, encoder, ct)

        return render_template("recommendation.html", predicted_style=predicted_style)

    return render_template("recommendation.html")

if __name__ == "__main__":
    app.run(debug=True)
