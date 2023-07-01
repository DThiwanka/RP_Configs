import tkinter as tk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Sample movie data
movies = {
    'Title': ['The Dark Knight', 'The Avengers', 'Interstellar', 'Inception', 'Pulp Fiction'],
    'Genre': ['Action, Crime, Drama', 'Action, Adventure, Sci-Fi', 'Adventure, Drama, Sci-Fi',
              'Action, Adventure, Sci-Fi', 'Crime, Drama, Thriller']
}

# Create a DataFrame from the movie data
df = pd.DataFrame(movies)

# Preprocess the data
df['Genre'] = df['Genre'].str.replace(',', ' ')

# Initialize the TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words='english')

# Compute the TF-IDF matrix
tfidf_matrix = tfidf.fit_transform(df['Genre'])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Function to get movie recommendations
def get_recommendations(title, cosine_sim):
    # Get the index of the movie that matches the title
    idx = df[df['Title'] == title].index[0]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 5 similar movies
    top_movies = sim_scores[1:6]

    # Get the titles of the recommended movies
    recommended_movies = [df['Title'][i[0]] for i in top_movies]

    return recommended_movies

# Create the GUI
window = tk.Tk()
window.title("Movie Recommendation System")

# Function to handle button click
def recommend_movies():
    movie_title = entry.get()
    recommendations = get_recommendations(movie_title, cosine_sim)
    output.delete('1.0', tk.END)  # Clear previous output
    output.insert(tk.END, f"Recommended movies for '{movie_title}':\n")
    for movie in recommendations:
        output.insert(tk.END, movie + "\n")

# Create GUI elements
label = tk.Label(window, text="Enter a movie title:")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Recommend", command=recommend_movies)
button.pack()

output = tk.Text(window, height=6, width=40)
output.pack()

# Start the GUI event loop
window.mainloop()
