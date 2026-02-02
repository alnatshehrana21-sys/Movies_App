# 🎬 My Movies Database - SQL & API Edition

Welcome to **My Movies Database**, a professional Python application that bridges the gap between raw data management and a visual web experience. This project serves as a robust engine for movie enthusiasts, allowing for automated data fetching, persistent SQL storage, and dynamic website generation.

## ✨ Features
* **Read (List & Display):** Retrieve all saved movies from a local SQLite database with formatted terminal output.
* **OMDb API Integration:** Add movies by title only—the app automatically fetches the release year, IMDb rating, and poster image URL.
* **SQL Persistence:** Utilizes SQLAlchemy to manage data in a structured relational database, replacing volatile JSON storage.
* **Website Generation:** Automatically transforms your local database into a beautiful, static HTML/CSS website with one command.
* **Analytics:** Calculate real-time statistics including average and median ratings of your entire collection.
* **Search & Random:** Find specific movies via case-insensitive search or let the app pick your "Movie for tonight" at random.

## 🛠️ Tech Stack
* **Backend:** Python 3
* **Database:** SQLite & SQLAlchemy (Object Relational Mapper)
* **API Integration:** OMDb API (Requests library)
* **Frontend:** HTML5 & CSS3
* **Version Control:** Git & GitHub

## 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/movie-database-app.git](https://github.com/YOUR_USERNAME/movie-database-app.git)
    cd movie-database-app
    ```

2.  **Install Dependencies:**
    ```bash
    pip install sqlalchemy requests
    ```

3.  **Setup API Key:**
    * Obtain your key from [omdbapi.com](https://www.omdbapi.com/).
    * Ensure the `API_KEY` variable in `movies.py` matches your active key.

4.  **Run the Application:**
    ```bash
    python movies.py
    ```

##
