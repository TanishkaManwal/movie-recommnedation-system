## 🎬 Movie Recommender System

A content-based movie recommendation system built with Streamlit.
👉 **[Live Demo](https://movie-recommnedation-system-gionvjqfftaov6upmhsi72.streamlit.app/)**  

This is a content-based movie recommendation system built with Python.
It helps users discover movies similar to the ones they like using a pre-computed similarity matrix and a clean Streamlit app.

📌 Features
🎥 Recommend movies based on a selected title

Uses the TMDB 5000 dataset

Fast recommendations with a pre-computed similarity .pkl

Auto-downloads required files from Google Drive

Streamlit app for easy, interactive UI

Click to view trailers

🚀 How It Works
The app uses:
tmdb_5000_movies.csv
tmdb_5000_credits.csv
A similarity matrix (similarity.pkl) is precomputed.

When you run app.py:
It checks if the required files exist.
If missing, it auto-downloads them using gdown.
Loads the data and displays similar movies for the selected movie.

🛠️ Tech Stack
Python
pandas, scikit-learn
pickle
gdown for automatic file downloads
Streamlit for the frontend
requests for API calls (OMDB)

📸 Screenshots
Movie selection & recommendations:
<img width="1887" height="904" alt="image" src="https://github.com/user-attachments/assets/12cbc8d3-699d-4a02-9984-af81718d815f" />
<img width="1802" height="475" alt="image" src="https://github.com/user-attachments/assets/f2933e70-6f7c-4bdb-80e5-e2bf6c7e1bb2" />
<img width="1807" height="738" alt="image" src="https://github.com/user-attachments/assets/54df0b83-6474-47fd-b536-7746d97a63d3" />

📦 Installation & Run
1️⃣ Clone the repo:
bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo

2️⃣ Install dependencies:
bash
pip install -r requirements.txt

3️⃣ Run the app:
bash
streamlit run app.py

❤️ Author
Made with ❤️ by Tanishka Manwal


