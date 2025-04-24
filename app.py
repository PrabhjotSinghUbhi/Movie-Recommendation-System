from flask import Flask, request, jsonify, render_template
import pickle
import requests

app = Flask(__name__)

# Load preprocessed data
movies = pickle.load(open('./movie_list.pkl', 'rb'))
similarity = pickle.load(open('./similarity.pkl', 'rb'))

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500"

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# Flask routes
@app.route('/')
def home():
    return render_template('index.html', movies=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    movie = request.form['movie']
    recommended_movie_names, recommended_movie_posters = recommend(movie)
    return jsonify({
        'names': recommended_movie_names,
        'posters': recommended_movie_posters
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
