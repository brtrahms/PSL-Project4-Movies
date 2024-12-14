import pandas as pd
import numpy as np
import requests

# Define the URL for movie data
myurl = "https://liangfgithub.github.io/MovieData/movies.dat?raw=true"

# Fetch the data from the URL
response = requests.get(myurl)

# Split the data into lines and then split each line using "::"
movie_lines = response.text.split('\n')
movie_data = [line.split("::") for line in movie_lines if line]

# Create a DataFrame from the movie data
movies = pd.DataFrame(movie_data, columns=['movie_id', 'title', 'genres'])
movies['movie_id'] = movies['movie_id'].astype(int)

# # Define the URL for movie data
# myurl = "https://liangfgithub.github.io/MovieData/ratings.dat?raw=true"

# # Fetch the data from the URL
# response = requests.get(myurl)

# # Split the data into lines and then split each line using "::"
# ratings_lines = response.text.split('\n')
# ratings_data = [line.split("::") for line in ratings_lines if line]

# # Create a DataFrame from the movie data
# ratings = pd.DataFrame(movie_data, columns=['UserID', 'MovieID', 'Rating', 'Timestamp'])
# ratings['MovieID'] = movies['MovieID'].astype(int)

# popular_movs = ratings.groupby('').count().sort_values(by='Rating', ascending=False)

genres = list(
    sorted(set([genre for genres in movies.genres.unique() for genre in genres.split("|")]))
)

def myIBCF(user):

    w = np.full(shape=100, fill_value=np.nan)

    for mov in user.keys():
        w[movies[movies['movie_id'] == mov].index] = user[mov]

    print("ratings: ", w)
    
    S = np.load('S_100x100.npy')

    ind = np.argwhere(~np.isnan(w)).T[0]
    
    for m in np.argwhere(np.isnan(w)).T[0]:
        w[m] = (S[m, ind] * w[ind]).sum() / S[m, ind].sum()

    top_movs = np.argsort(w[-ind])

    top_movs = movies['movie_id'].loc[top_movs[:10]].to_numpy()

    print("movies: ", top_movs)
    
    return movies.set_index('movie_id').loc[top_movs].reset_index()

def get_displayed_movies():
    return movies.head(100)

def get_recommended_movies(new_user_ratings):
    return movies.head(10)

def get_popular_movies(genre: str):
    if genre == genres[1]:
        return movies.head(10)
    else: 
        return movies[10:20]