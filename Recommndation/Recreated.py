import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Load the existing data (if any) from a CSV file or start with an empty DataFrame
try:
    existing_data = pd.read_csv("existing_data.csv")
except FileNotFoundError:
    existing_data = pd.DataFrame(columns=['ID', 'Name', 'Age', 'Comments'])

# Create an instance of the model or load the existing model
model = LogisticRegression(max_iter=1000, solver='lbfgs') if existing_data.empty or len(existing_data['Comments'].unique()) < 2 else LogisticRegression(max_iter=1000, solver='lbfgs').fit(
    existing_data[['ID', 'Age']], existing_data['Comments']
)

# Input loop
while True:
    # Accept user input
    id_input = input("Enter ID (or 'q' to quit): ")
    if id_input.lower() == 'q':
        break

    name_input = input("Enter Name: ")
    age_input = int(input("Enter Age: "))
    comments_input = input("Enter Comments: ")

    # Create a new row for the input data
    new_data = pd.DataFrame({
        'ID': [int(id_input)],
        'Name': [name_input],
        'Age': [age_input],
        'Comments': [comments_input]
    })

    # Append the new data to the existing data
    existing_data = pd.concat([existing_data, new_data], ignore_index=True)

    # Check if there are at least two distinct classes in the target variable
    unique_classes = existing_data['Comments'].unique()
    if len(unique_classes) >= 2:
        # Scale the data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(existing_data[['ID', 'Age']])

        # Retrain the model with the scaled data
        model.fit(scaled_data, existing_data['Comments'])

        # Make predictions
        input_data = scaled_data[-1:]  # Use the latest row as input for prediction
        predicted_class = model.predict(input_data)
        print("Predicted class:", predicted_class)

    # Save the updated data to a CSV file
    existing_data.to_csv("existing_data.csv", index=False)

# Once the loop ends, you can use the trained model for predictions or other tasks
