# model_training.py
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

def train_model(preprocessed_data):
    features = preprocessed_data.iloc[:, :-1]
    labels = preprocessed_data.iloc[:, -1]

    # Split the dataset into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Train a decision tree classifier
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = model.score(X_val, y_val)
    print("Model accuracy:", accuracy)

    return model
