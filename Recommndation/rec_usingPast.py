import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from imblearn.over_sampling import RandomOverSampler

# Load the CSV file
data = pd.read_csv("./csvfiles/fashion_data_forHkz_run.csv")

# Perform label encoding on the target variable
encoder = LabelEncoder()
data["OutfitChoiceEncoded"] = encoder.fit_transform(data["OutfitChoice"])

# Split the data into features and target
X = data.drop(["OutfitChoice"], axis=1)
y = data["OutfitChoiceEncoded"]

# Define the column transformer for one-hot encoding
ct = ColumnTransformer(
    transformers=[("encoder", OneHotEncoder(handle_unknown='ignore'), ["UserID", "Age", "Gender", "FashionType"])],
    remainder="passthrough"
)

# Apply the column transformer on the input features
X_encoded = ct.fit_transform(X)

# Handle class imbalance using RandomOverSampler
oversampler = RandomOverSampler(random_state=42)
X_resampled, y_resampled = oversampler.fit_resample(X_encoded, y)

# Create a random forest classifier
classifier = RandomForestClassifier()

# Define the hyperparameter grid
param_grid = {
    "n_estimators": [100, 200, 300],  # Number of trees in the forest
    "max_depth": [None, 5, 10, 20],  # Maximum depth of the tree
    "min_samples_split": [2, 5, 10],  # Minimum number of samples required to split an internal node
    "min_samples_leaf": [1, 2, 4],  # Minimum number of samples required to be at a leaf node
}

# Perform grid search with stratified k-fold cross-validation to find the best hyperparameters
cv = StratifiedKFold(n_splits=2)
grid_search = GridSearchCV(estimator=classifier, param_grid=param_grid, cv=cv)
grid_search.fit(X_resampled, y_resampled)

# Get the best model
best_classifier = grid_search.best_estimator_

# Streamlit GUI
st.title("Fashion Style Predictor")
st.write("Enter the details below to predict the fashion style.")

# Get user input
user_id = st.text_input("User ID", "")
age = st.selectbox("Age", data["Age"].unique())
gender = st.selectbox("Gender", data["Gender"].unique())
fashion_type = st.selectbox("Fashion Type", data["FashionType"].unique())

# Encode the user input
input_data = pd.DataFrame([[user_id, age, gender, fashion_type]], columns=["UserID", "Age", "Gender", "FashionType"])
input_data_encoded = ct.transform(input_data)

# Make prediction
prediction = best_classifier.predict(input_data_encoded)
predicted_style = encoder.inverse_transform(prediction)[0]

st.write("Predicted Fashion Style:", predicted_style)

# Calculate cosine similarity between fashion styles
outfit_encodings = ct.transform(X_resampled)
cosine_sim = cosine_similarity(outfit_encodings)

# Find index of predicted style in the dataframe
predicted_style_index = data[data["OutfitChoice"] == predicted_style].index[0]

# Get similar fashion styles based on cosine similarity
similar_styles_indices = cosine_sim[predicted_style_index].argsort()[::-1][1:4]
recommended_styles = data.loc[similar_styles_indices, "OutfitChoice"].tolist()

st.write("Recommended Fashion Styles:", recommended_styles)
