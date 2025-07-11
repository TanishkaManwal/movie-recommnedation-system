# 🎬 Movie Recommendation System

This project is a **content-based movie recommendation system** built with **Python**.  
It helps users discover movies similar to the ones they like by using a pre-computed similarity matrix.

---

## 📂 Features

- Recommend movies based on selected titles
- Uses TMDB 5000 dataset
- Pre-computed similarity matrix for fast recommendations
- Streamlit app for easy user interaction *(if you use Streamlit)*
- Auto-downloads large files from Google Drive at runtime

---

## 🚀 How it works

- The app uses a TMDB dataset (`tmdb_5000_credits.csv` and `tmdb_5000_movies.csv`).
- It builds a similarity matrix (or uses a pre-computed `.pkl`).
- When you run `app.py`, it:
  - Checks if `similarity.pkl` is present
  - If not, downloads it from Google Drive automatically using `gdown`
- Then it loads the matrix and generates recommendations.

---

## 🛠️ Tech Stack

- **Python**
- **pandas**, **scikit-learn**
- **pickle**
- **gdown** (for downloading files)
- *(Optional)* **Streamlit** for the frontend

---

## 📦 Installation

1. **Clone the repo:**

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo

