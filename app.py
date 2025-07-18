import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown   

# -------------------- Download if missing --------------------
if not os.path.exists('movie_list.pkl'):
    url = 'https://drive.google.com/uc?id=1LpeIhcQ9bBtlYioAH1MLV2G-SjeL3ZuX'
    gdown.download(url, 'movie_list.pkl', quiet=False)

if not os.path.exists('similarity.pkl'):
    url = 'https://drive.google.com/uc?id=1lGNXc65l0zU5M1y1t1lY74yLEueuAjTI'
    gdown.download(url, 'similarity.pkl', quiet=False)
    
# # Debug: check files
# st.write("Current working directory:", os.getcwd())
# st.write("Files in current directory:", os.listdir())
# -------------------- Load Data --------------------
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

OMDB_API_KEY = "e05c0078"

# -------------------- Helpers --------------------
@st.cache_data
def fetch_movie_details(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return {
        'poster': data.get('Poster', 'https://via.placeholder.com/300x450?text=No+Poster'),
        'plot': data.get('Plot', 'No plot available'),
        'year': data.get('Year', 'N/A'),
        'rating': data.get('imdbRating', 'N/A')
    }

def get_youtube_search_url(movie_name):
    query = movie_name + " trailer"
    return f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"

def recommend(movie, min_rating=None):
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
    for i in distances[1:]:
        title = movies.iloc[i[0]].title
        details = fetch_movie_details(title)
        if min_rating:
            try:
                if float(details['rating']) < min_rating:
                    continue
            except:
                continue
        youtube_url = get_youtube_search_url(title)
        recommendations.append({
            'title': title,
            'poster': details['poster'],
            'plot': details['plot'],
            'year': details['year'],
            'rating': details['rating'],
            'youtube_url': youtube_url
        })
        if len(recommendations) >= 5:
            break
    return recommendations

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")



st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
        }
        .movie-card {
            background-color: #111;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            transition: 0.3s;
        }
        .movie-card:hover {
            transform: scale(1.05);
            box-shadow: 0 0 10px #f39c12;
        }
    </style>
""", unsafe_allow_html=True)
st.title("🎬 Movie Recommender System")
st.markdown("Pick a movie, see recommendations & build your watchlist!")

# Sidebar Watchlist

# Search Bar
movie_input = st.text_input("🔍 Search for a movie:", "")

# Or fallback to dropdown if empty
if not movie_input:
    selected_movie = st.selectbox("Or pick from list:", sorted(movies['title'].values))
else:
    matches = movies[movies['title'].str.contains(movie_input, case=False, na=False)]
    if not matches.empty:
        selected_movie = matches.iloc[0].title
    else:
        st.warning("No movie found. Try a different name.")
        selected_movie = None

# Filters
min_rating = st.slider("Minimum IMDB Rating:", 0.0, 10.0, 0.0, 0.5)

# Show Recommendations
if selected_movie and st.button("🔍 Show Recommendations"):
    recommendations = recommend(selected_movie, min_rating)

    if not recommendations:
        st.error("❌ No recommendations found.")
    else:
        st.markdown("## 💡 You Might Also Like:")
        cols = st.columns(5)
        for i, rec in enumerate(recommendations):
            with cols[i]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                st.image(rec['poster'], use_container_width=True)
                st.markdown(f"**{rec['title']}** ({rec['year']})")
                st.markdown(f"⭐ IMDB: {rec['rating']}")
                st.markdown(f"*{rec['plot']}*")
                st.markdown(f"[▶ Watch Trailer]({rec['youtube_url']})")

                st.markdown('</div>', unsafe_allow_html=True)


