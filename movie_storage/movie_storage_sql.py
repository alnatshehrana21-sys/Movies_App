"""
Handles SQLite database operations for the Movie App.
Uses SQLAlchemy to execute raw SQL queries.
"""
from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)

def init_db():
    """Initializes the movies table if it doesn't exist, including a poster column."""
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster TEXT
            )
        """))
        connection.commit()

def list_movies():
    """Retrieve all movies from the database as a dictionary of dictionaries."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()

    # Returns data in a format compatible with the main app logic
    return {
        row[0]: {
            "year": row[1], 
            "rating": row[2], 
            "poster": row[3]
        } for row in movies
    }

def add_movie(title, year, rating, poster):
    """Add a new movie to the database with poster info."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies (title, year, rating, poster) "
                     "VALUES (:title, :year, :rating, :poster)"), 
                {"title": title, "year": year, "rating": rating, "poster": poster}
            )
            connection.commit()
        except Exception as e:
            print(f"Database Error: {e}")

def delete_movie(title):
    """Delete a movie from the database by title."""
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"),
            {"title": title}
        )
        connection.commit()
        return result.rowcount > 0

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating WHERE title = :title"),
            {"title": title, "rating": rating}
        )
        connection.commit()
        return result.rowcount > 0

# Ensure the database is ready when the module is loaded
init_db()