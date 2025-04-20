import pickle
import streamlit as st
import requests


# function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500"


# function to recommend movies
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


# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎬 Movie Recommender System')

movies = pickle.load(open('./movie_list.pkl', 'rb'))
similarity = pickle.load(open('./similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🎥 Type or select a movie from the dropdown",
    movie_list
)

if st.button('🚀 Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.markdown("## 🎞️ Recommended Movies for You")
    cols = st.columns(5)  # create 5 columns

    for idx, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[idx], use_container_width=True)  # ✅ updated
            st.markdown(f"**{recommended_movie_names[idx]}**", unsafe_allow_html=True)
