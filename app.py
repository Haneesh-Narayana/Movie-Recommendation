from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import requests

app = Flask(__name__)

# Load the movie dataset and similarity model
with open('movie_dataset.pkl', 'rb') as f:
    df = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

OMDB_API_KEY = '3caced6'
OMDB_API_URL = 'http://www.omdbapi.com/?i=tt3896198&apikey=3caced6'

def get_movie_poster(title):
    response = requests.get(OMDB_API_URL, params={'t': title, 'apikey': OMDB_API_KEY})
    data = response.json()
    if data['Response'] == 'True':
        return data.get('Poster')
    return None

def recommend_movie(movie_name):
    try:
        movie_index = df[df['title'] == movie_name].index[0]
        sim_movies = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda vector: vector[1])
        recommendations = []
        for i in sim_movies[1:6]:
            movie_title = df.iloc[i[0]].title
            poster_url = get_movie_poster(movie_title)
            recommendations.append({'title': movie_title, 'similarity': round(i[1] * 100, 2), 'poster': poster_url})
        return recommendations
    except IndexError:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form['movie_name']
    recommendations = recommend_movie(movie_name)
    if recommendations is None:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
