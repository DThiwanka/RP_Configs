import random
from tkinter import *
import requests
import json

# Sample fashion items
fashion_items = [
    "T-Shirt",
    "Jeans",
    "Dress",
    "Shoes",
    "Sunglasses",
    "Handbag",
    "Watch",
    "Hat"
]

# Generate random user behavior data (this should be replaced with real data)
user_behavior = {
    "user1": random.sample(fashion_items, random.randint(1, 4)),
    "user2": random.sample(fashion_items, random.randint(1, 4)),
    "user3": random.sample(fashion_items, random.randint(1, 4)),
    # Add more users and their behavior here
}

# Define collaborative filtering recommender function
def collaborative_filtering(user_behavior):
    # Process user behavior data and generate recommendations using AI libraries
    # Replace this function with your own implementation using AI libraries

    # For this example, we'll return random fashion items not in the user's past behavior
    all_items = set(fashion_items)
    user_items = set(user_behavior)
    recommendations = list(all_items - user_items)

    return recommendations

# Function to handle button click event
def recommend_fashion():
    # Get the user and behavior from the input fields
    user = user_entry.get()
    behavior = behavior_entry.get().split(',')

    # Add user behavior to the existing data
    user_behavior[user] = behavior

    # Get recommendations for the user
    recommendations = collaborative_filtering(user_behavior)

    # Display the recommendations in the GUI
    recommendations_text.delete('1.0', END)
    for item in recommendations:
        recommendations_text.insert(END, f"- {item}\n")

    # Make a POST request to the API to store user behavior (Replace URL with the actual API endpoint)
    url = "http://localhost:5000/recommendations"
    data = {
        "user": user,
        "behavior": behavior
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.json())

# Create GUI window
window = Tk()
window.title("Fashion Recommendation System")

# Create and position input fields
user_label = Label(window, text="User:")
user_label.grid(row=0, column=0, padx=10, pady=10)
user_entry = Entry(window)
user_entry.grid(row=0, column=1, padx=10, pady=10)

behavior_label = Label(window, text="Behavior (comma-separated):")
behavior_label.grid(row=1, column=0, padx=10, pady=10)
behavior_entry = Entry(window)
behavior_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and position recommendation display area
recommendations_label = Label(window, text="Recommendations:")
recommendations_label.grid(row=2, column=0, padx=10, pady=10)
recommendations_text = Text(window, width=30, height=10)
recommendations_text.grid(row=2, column=1, padx=10, pady=10)

# Create and position recommendation button
recommend_button = Button(window, text="Recommend", command=recommend_fashion)
recommend_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the GUI
window.mainloop()
