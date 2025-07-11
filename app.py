import streamlit as st
import pickle
import pandas as pd
import gdown
import os
import requests

# ------------------------ Download Required Files ------------------------

# Download similarity.pkl
if not os.path.exists('similarity.pkl'):
    url = 'https://drive.google.com/uc?id=1lGNXc65l0zU5M1y1t1lY74yLEueuAjTI'
    gdown.download(url, 'similarity.pkl', quiet=False)

# Download tmdb_movie.csv
if not os.path.exists('tmdb_movie.csv'):
    url = 'https://drive.google.com/uc?id=1BvfFPF657IYap-VGntvVuxljA1_U4jy6'
    gdown.download(url, 'tmdb_movie.csv', quiet=False)

# Download tmdb_credits.csv
if not os.path.exists('tmdb_credits.csv'):
    url = 'https://drive.google.com/uc?id=1dxwhOzH60XXLTvghKbcK7_MUuHeGTTQE'
    gdown.download(url, 'tmdb_credits.csv', quiet=False)

# Download movie_list.pkl
if not os.path.exists('movie_list.pkl'):
    url = 'https://drive.google.com/uc?id=1LpeIhcQ9bBtlYioAH1MLV2G-SjeL3ZuX'
    gdown.download(url, 'movie_list.pkl', quiet=False)

# ------------------------ Load Model & Data ------------------------

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

OMDB_API_KEY = "e05c0078"

def fetch_poster(movie_title):
    try:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if 'Poster' in data and data['Poster'] != 'N/A':
            return data['Poster']
    except:
        pass
    return "https://via.placeholder.com/300x450?text=No+Poster"

def get_youtube_search_url(movie_name):
    query = movie_name + " trailer"
    return f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"

def recommend(movie):
    movie = movie.lower()
    movie_index = movies[movies['title'].str.lower() == movie].index
    if len(movie_index) == 0:
        return []
    index = movie_index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )
    recommendations = []
    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        poster_url = fetch_poster(title)
        youtube_url = get_youtube_search_url(title)
        recommendations.append({
            'title': title,
            'poster': poster_url,
            'youtube_url': youtube_url
        })
    return recommendations

# ------------------------ Streamlit UI ------------------------

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
        }
        .movie-card {
            background-color: #222;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            transition: 0.3s;
        }
        .movie-card:hover {
            transform: scale(1.03);
            box-shadow: 0 0 10px #f39c12;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Pick a movie and get recommendations instantly!</p>", unsafe_allow_html=True)

selected_movie = st.selectbox("🎥 Choose a movie:", movies['title'].values)

if st.button("🔍 Show Recommendations"):
    recommendations = recommend(selected_movie)

    if not recommendations:
        st.error("❌ Movie not found or no recommendations available.")
    else:
        st.markdown("## 💡 You Might Also Like:")
        cols = st.columns(5)
        for i, rec in enumerate(recommendations):
            with cols[i]:
                st.image(rec['poster'], use_container_width=True)
                st.markdown(f"**{rec['title']}**")
                st.markdown(f"[▶ Watch Trailer]({rec['youtube_url']})")

st.markdown("""
---
<p style='text-align:center;'>Made with ❤️ using Streamlit</p>
""", unsafe_allow_html=True)
