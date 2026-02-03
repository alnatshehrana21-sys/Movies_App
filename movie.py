"""
Main program for the Movie App.
Handles User Interface, API fetching from OMDb, and local SQL storage.
"""

import requests
import random
from movie_storage import movie_storage_sql as storage # Refactored import

# API Configuration - Ba8866e7 confirmed from user email
API_KEY = "ba8866e7"

# --- Input Helpers ---

def input_nonempty(prompt):
    """Ask until a non-empty string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Try again.")

def input_float(prompt, min_val=0, max_val=10):
    """Ask until a valid float within limits is entered."""
    while True:
        value = input(prompt).strip()
        try:
            num = float(value)
            if min_val <= num <= max_val:
                return num
            print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# --- Command Functions ---

def command_list_movies():
    """Retrieve and display all movies from the SQL database."""
    movies = storage.list_movies()
    print(f"\n{len(movies)} movies in total")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): Rating {data['rating']}")

def command_add_movie():
    """Fetches movie data from OMDb API and adds it to the database."""
    title_query = input_nonempty("Enter movie name to add: ")
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title_query}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            actual_title = data.get("Title")
            year = int(data.get("Year")[:4])
            raw_rating = data.get("imdbRating")
            rating = float(raw_rating) if raw_rating != "N/A" else 0.0
            poster_url = data.get("Poster")

            storage.add_movie(actual_title, year, rating, poster_url)
            print(f"Successfully added: {actual_title} ({year})")
        else:
            print(f"API Error: {data.get('Error')}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Check your internet connection.")

def command_delete_movie():
    """Delete a movie by title."""
    title = input_nonempty("Enter movie name to delete: ")
    if storage.delete_movie(title):
        print(f"Movie '{title}' deleted.")
    else:
        print(f"Movie '{title}' not found.")

def command_update_movie():
    """Update an existing movie's rating in the SQL database."""
    title = input_nonempty("Enter movie name to update: ")
    if title not in storage.list_movies():
        print(f"Movie '{title}' not found.")
        return
    new_rating = input_float("Enter new rating (0-10): ")
    if storage.update_movie(title, new_rating):
        print(f"Movie '{title}' updated.")

def command_statistics():
    """Calculate and display analytics."""
    movies = storage.list_movies()
    if not movies:
        print("Database is empty.")
        return
    ratings = [data['rating'] for data in movies.values()]
    avg = sum(ratings) / len(ratings)
    sorted_ratings = sorted(ratings)
    mid = len(sorted_ratings) // 2
    median = (sorted_ratings[mid] if len(sorted_ratings) % 2 != 0
              else (sorted_ratings[mid-1] + sorted_ratings[mid]) / 2)
    print(f"\n--- Statistics ---")
    print(f"Average Rating: {avg:.2f}")
    print(f"Median Rating: {median:.2f}")

def command_random_movie():
    """Selects and prints a random movie from the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return
    title, data = random.choice(list(movies.items()))
    print(f"Your movie for tonight: {title} ({data['year']}) - Rating: {data['rating']}")

def command_search_movies():
    """Search for movies locally by title."""
    query = input_nonempty("Search for: ").lower()
    movies = storage.list_movies()
    found = False
    for title, data in movies.items():
        if query in title.lower():
            print(f"{title} ({data['year']}): {data['rating']}")
            found = True
    if not found:
        print("No matches found.")

def command_sorted_movies():
    """Lists movies sorted by rating in descending order."""
    movies = storage.list_movies()
    if not movies:
        print("No movies in database.")
        return
    sorted_movies = sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True)
    print("\nMovies sorted by rating (best first):")
    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']}")

def generate_website():
    """Generates index.html using the template and SQL data."""
    try:
        with open("static/index_template.html", "r", encoding="utf-8") as file:
            template_content = file.read()
    except FileNotFoundError:
        print("Error: static/index_template.html not found.")
        return
    movies = storage.list_movies()
    movie_grid_html = ""
    for title, data in movies.items():
        movie_grid_html += '<li>\n  <div class="movie">\n'
        movie_grid_html += f'    <img class="movie-poster" src="{data["poster"]}" alt="{title} poster"/>\n'
        movie_grid_html += f'    <div class="movie-title">{title}</div>\n'
        movie_grid_html += f'    <div class="movie-year">{data["year"]}</div>\n'
        movie_grid_html += '  </div>\n</li>\n'
    new_content = template_content.replace("__TEMPLATE_TITLE__", "My Movies Database")
    new_content = new_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(new_content)
    print("Website was generated successfully.")

# --- Main Logic ---

def main():
    actions = {
        "0": ("Exit", None),
        "1": ("List movies", command_list_movies),
        "2": ("Add movie (API)", command_add_movie),
        "3": ("Delete movie", command_delete_movie),
        "4": ("Update movie", command_update_movie),
        "5": ("Stats", command_statistics),
        "6": ("Random movie", command_random_movie),
        "7": ("Search movie", command_search_movies),
        "8": ("Sorted by rating", command_sorted_movies),
        "9": ("Generate website", generate_website)
    }
    print("********** My Movies App: SQL + API + HTML **********")
    while True:
        print("\nMenu:")
        for key in sorted(actions.keys(), key=int):
            label, _ = actions[key]
            print(f"{key}. {label}")
        choice = input("\nEnter choice: ").strip()
        if choice == "0":
            print("Bye!")
            break
        if choice in actions:
            _, func = actions[choice]
            func()
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()