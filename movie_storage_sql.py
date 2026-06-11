from sqlalchemy import create_engine, text
import requests


# Define the database URL
DB_URL = "sqlite:///movies.db"

# Define the web url
WEB_URL = "http://www.omdbapi.com/?apikey=8b28d4a6&t="

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            picture TEXT NOT NULL
        )
    """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, picture FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "picture": row[3]} for row in movies}


def add_movie(title):
    """Add a new movie to the database."""
    url = WEB_URL + title
    response = requests.get(url, timeout=5)
    data = response.json()

    with engine.connect() as connection:
        try:
            params = {'title': data['Title'], 'year': data['Year'],
                      'rating': data['Ratings'][0]['Value'],'picture': data['Poster']}

            connection.execute(text("INSERT INTO movies (title, year, rating, picture) "
                                    "VALUES (:title, :year, :rating, :picture)"), params)

            connection.commit()

            print(f"Movie '{title}' added successfully.")


        except requests.exceptions.RequestException as api_error:
            print(f"API- or network-Error for '{title}': {api_error}")

        except KeyError as data_error:
            print(f"Error: Missing data for '{title}': {data_error}")

def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"),{"title":title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")

        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"),
                               {'rating':rating, 'title':title})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")

        except Exception as e:
            print(f"Error: {e}")