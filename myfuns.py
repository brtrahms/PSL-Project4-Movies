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

def myIBCF(w):

    Sim = np.load('S_3706x30.npy')

    rated = ~np.isnan(w)
    
    for m in np.argwhere(~rated).T[0]:

        ind = ~np.isnan(Sim[m]) & rated
        
        w[m] = (Sim[m, ind] * w[ind]).sum() / Sim[m, ind].sum()
    
    top_movs = np.argsort(w)[::-1]

    mask = np.isnan(w)

    top_movs = top_movs[~mask[top_movs] & ~rated[top_movs]]
    
    top_movs = np.argsort(np.where(np.isnan(w), 0, w))[::-1]
    
    top_movs = top_movs[~np.isin(top_movs, np.argwhere(rated))]

    top_movs = np.char.add('m', R.columns[top_movs[:10]].to_numpy().astype(str))

    return np.concat((top_movs, np.char.add('m', popular_movs.index.to_numpy()[:10 - len(top_movs)].astype(str))))
    
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