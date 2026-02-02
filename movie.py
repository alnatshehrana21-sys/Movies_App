"""
Main program for the Movie App.
Handles User Interface, API fetching from OMDb, and local SQL storage.
"""
import requests
from movie_storage import movie_storage_sql as storage

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

            # Extract and clean data
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
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def command_delete_movie():
    """Delete a movie by title."""
    title = input_nonempty("Enter movie name to delete: ")
    if storage.delete_movie(title):
        print(f"Movie '{title}' deleted.")
    else:
        print(f"Movie '{title}' not found.")

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

def generate_website():
    """Generates index.html using the template and SQL data."""
    # Load the template file
    try:
        with open("static/index_template.html", "r", encoding="utf-8") as file:
            template_content = file.read()
    except FileNotFoundError:
        print("Error: index_template.html not found.")
        return

    # Fetch data from SQL
    movies = storage.list_movies()

    # Build the HTML string for the movie grid
    movie_grid_html = ""
    for title, data in movies.items():
        movie_grid_html += '<li>\n'
        movie_grid_html += '  <div class="movie">\n'
        movie_grid_html += f'    <img class="movie-poster" src="{data["poster"]}" alt="{title} poster"/>\n'
        movie_grid_html += f'    <div class="movie-title">{title}</div>\n'
        movie_grid_html += f'    <div class="movie-year">{data["year"]}</div>\n'
        movie_grid_html += '  </div>\n'
        movie_grid_html += '</li>\n'

    # Replace placeholders in the template
    new_content = template_content.replace("__TEMPLATE_TITLE__", "My Movies Database")
    new_content = new_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    # Write the output file
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(new_content)

    print("Website was generated successfully.")

# --- Main Logic ---

def main():
    actions = {
        "0": ("Exit", None),
        "1": ("List movies", command_list_movies),
        "2": ("Add movie (via OMDb API)", command_add_movie),
        "3": ("Delete movie", command_delete_movie),
        "5": ("Stats", command_statistics),
        "9": ("Generate website", generate_website)
    }

    print("********** My Movies App: SQL + API + HTML **********")

    while True:
        print("\nMenu:")
        for key in sorted(actions.keys()):
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
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()