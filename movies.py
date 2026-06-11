import random
import statistics
import sys
import movie_storage_sql as storage
import website_generator


def exit_program():
    """Exits the program"""
    sys.exit()


def show_sorted_movies():
    """Prints all movies sorted by rating"""
    movies = storage.list_movies()
    title_rating_dict = {}
    for title, information in movies.items():
        title_rating_dict[title] = information["rating"]

    sorted_movies = sorted(title_rating_dict.items(), key=lambda x: x[1], reverse=True)

    for title, rating in sorted_movies:
        print(f"{title}: {rating}")


def search_movie():
    """Prints the movie with all stats the user asks for"""
    movies = storage.list_movies()
    search = input("Which movie do you search for?: ").lower()
    for title, information in movies.items():
        if search in title.lower():
            print(f"{title}: rating {information['rating']}, release year {information['year']}")



def add_movie():
    """
    Prompts the user for movie details and adds the movie to the database.
    """

    input_validation = True

    while input_validation:
        title = input("Enter the name of the movie: ")
        if title == "":
            print("Please enter a valid movie title.")
            continue

        input_validation = False
        storage.add_movie(title)


def update_movie():
    """
    Allows the user to change the rating of an existing movie.
    """
    movies = storage.list_movies()
    title = input("Which movie do you want to update? ")

    if title in movies:
        input_validation = True
        while input_validation:
            try:
                new_rating = float(input(f"New rating for '{title}': "))
                input_validation = False
                storage.update_movie(title, new_rating)

            except ValueError:
                print("Please enter a number.")

    else:
        print(
            f"Error: The movie '{title}' is not in the database."
        )


def random_movie():
    """Shows a random movie with all stats"""
    movies = storage.list_movies()
    title, information = random.choice(list(movies.items()))
    print(f"This is your random movie: {title} (rating: {information['rating']}, release year: {information['year']})")


def delete_movie():
    """Takes a user input and calls the delete_movie function in movie_storage_sql"""
    title = input("Which movie do you want to delete? ")
    storage.delete_movie(title)


def show_stats():
    """The function calculates and prints average, median, best and worst rated movies"""
    movies = storage.list_movies()

    ratings = []
    for title, information in movies.items():
        ratings.append(information["rating"])

    average_rating = round(sum(ratings) / len(ratings), 2)

    median_rating = statistics.median(
        ratings
    )  # needs module "statistics", is able to calculate the median

    best_rating = max(ratings)
    best_movies = [
        title for title, rating in movies.items() if rating["rating"] == best_rating
    ]  # list comprehension

    worst_rating = min(ratings)
    worst_movies = [
        title for title, rating in movies.items() if rating["rating"] == worst_rating
    ]  # list comprehension

    print(f"The average rating is: {average_rating}")
    print(f"The median rating is: {median_rating}")
    print(f"The movie with the best rating is: {best_movies}")
    print(f"The movie with the worst rating is: {worst_movies}")


def show_all_movies_and_ratings():
    """Show all movies and their rating"""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def generate_website():
    """Calls function to load the html template in website_generator.py"""
    movies = storage.list_movies()
    website_generator.load_html_template(movies)


def main():
    """This program is a movie database application that allows users to add, delete, update,
    and view movies along with their ratings and release years. Users can also view statistics about the movies,
    get a random movie recommendation, and search for movies by title."""
    action_list = {
        "Exit" : exit_program,
        "List movies" : show_all_movies_and_ratings,
        "Add movie" : add_movie,
        "Delete movie" : delete_movie,
        "Update movie" : update_movie,
        "Stats" : show_stats,
        "Random movie" : random_movie,
        "Search movie" : search_movie,
        "Movies sorted by rating" : show_sorted_movies,
        "Generate website" : generate_website,
    }


    while True:
        print("******** My Movies Database **********\n")
        print("Menu:")

        for menu_number, action in action_list.items():
            print(menu_number)

        user_input = input(
            "What do you wanna do? "
        )

        try:
            action_list[user_input]()

        except KeyError:
            print("Unknown action. Please enter a valid action.")



if __name__ == "__main__":
    main()
