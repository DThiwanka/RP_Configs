import tkinter as tk
import pandas as pd
import numpy as np
import scipy.sparse as sparse
import implicit

# Sample movie data
movies = {
    'Title': ['The Dark Knight', 'The Avengers', 'Interstellar', 'Inception', 'Pulp Fiction'],
    'Genre': ['Action, Crime, Drama', 'Action, Adventure, Sci-Fi', 'Adventure, Drama, Sci-Fi',
              'Action, Adventure, Sci-Fi', 'Crime, Drama, Thriller']
}

# Sample user-movie ratings data
ratings = {
    'User': [1, 1, 2, 2, 3, 3],
    'Title': ['The Dark Knight', 'The Avengers', 'The Dark Knight', 'Interstellar', 'Inception', 'Pulp Fiction'],
    'Rating': [5, 4, 4.5, 3.5, 5, 4]
}

# Create a DataFrame from the movie data
movies_df = pd.DataFrame(movies)

# Create a DataFrame from the user-movie ratings data
ratings_df = pd.DataFrame(ratings)

# Create a mapping between movie titles and movie IDs
movies_df['MovieID'] = movies_df.index
movies_mapping = dict(zip(movies_df['Title'], movies_df['MovieID']))

# Create a mapping between user IDs and movie ratings
ratings_df['UserID'] = ratings_df['User']
ratings_df['MovieID'] = ratings_df['Title'].map(movies_mapping)

# Create a sparse user-movie ratings matrix
ratings_matrix = sparse.csr_matrix((ratings_df['Rating'], (ratings_df['UserID'], ratings_df['MovieID'])))

# Perform matrix factorization with ALS
model = implicit.als.AlternatingLeastSquares(factors=50)
model.fit(ratings_matrix)

# Function to get movie recommendations
def get_recommendations(user_id, model, movies_df, num_recommendations=5):
    # Get the user's movie ratings
    user_ratings = ratings_matrix[user_id, :]

    # Perform item-based collaborative filtering to get similar movies
    similar_movies = model.similar_items(user_ratings.indices, N=num_recommendations+1)

    # Get the movie IDs of the similar movies
    similar_movie_ids = [movie_id for movie_id, _ in similar_movies]

    # Check if there are any valid similar movie IDs
    if similar_movie_ids:
        # Get the titles of the recommended movies
        recommended_movies = movies_df.loc[similar_movie_ids, 'Title'].tolist()[1:]
    else:
        recommended_movies = []

    return recommended_movies

# Create the GUI
window = tk.Tk()
window.title("Movie Recommendation System")

# Function to handle button click
def recommend_movies():
    user_id = int(entry.get())
    recommendations = get_recommendations(user_id, model, movies_df)
    output.delete('1.0', tk.END)  # Clear previous output
    output.insert(tk.END, f"Recommended movies for User {user_id}:\n")
    for movie in recommendations:
        output.insert(tk.END, movie + "\n")

# Create GUI elements
label = tk.Label(window, text="Enter a user ID:")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Recommend", command=recommend_movies)
button.pack()

output = tk.Text(window, height=6, width=40)
output.pack()

# Start the GUI event loop
window.mainloop()
