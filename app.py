import streamlit as st
import pickle
import pandas as pd
import requests

# ---------------------------- Load Model & Data ----------------------------
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# -------------------------- OMDb API for Posters --------------------------
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

# -------------------------- YouTube Search URL ----------------------------
def get_youtube_search_url(movie_name):
    query = movie_name + " trailer"
    return f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"

# -------------------------- Recommend Function ----------------------------
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

# ---------------------------- Streamlit UI --------------------------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Styling
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

# Title
st.markdown("<h1 style='text-align:center;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Pick a movie and get recommendations instantly!</p>", unsafe_allow_html=True)

# Movie Selector
selected_movie = st.selectbox("🎥 Choose a movie:", movies['title'].values)

# Button to trigger recommendations
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

# ---------------------------- Footer --------------------------------------
st.markdown("""
---
<p style='text-align:center;'>Made with ❤️ using Streamlit</p>
""", unsafe_allow_html=True)
