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
    # can be used to find the best anf worst movies
    for title, information in movies.items():
        rating = information["rating"]
        ratings.append(rating)

    ratings_as_float =[]
    # is needed to sum all the ratings
    for rating in ratings:
        split_rating = rating.split("/")
        ratings_as_float.append(float(split_rating[0]))

    average_rating = round(sum(ratings_as_float) / len(ratings_as_float), 2)

    median_rating = statistics.median(
        ratings_as_float
    )  # needs module "statistics", is able to calculate the median

    best_rating = max(ratings)
    best_movies = []
    for title, information in movies.items():
        if information["rating"] == best_rating:
            best_movies.append(title)

    worst_rating = min(ratings)
    worst_movies = []
    for title, information in movies.items():
        if information["rating"] == worst_rating:
            worst_movies.append(title)

    print(f"The average rating is: {average_rating}/10")
    print(f"The median rating is: {median_rating}/10")
    print(f"The movie with the best rating is: {best_movies}: {best_rating}")
    print(f"The movie with the worst rating is: {worst_movies}: {worst_rating}")


def show_all_movies_and_ratings():
    """Show all movies and their rating"""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def generate_website():
    """Calls function to load the HTML template in website_generator.py"""
    movies = storage.list_movies()
    website_generator.load_html_template(movies)


def main():
    """This program is a movie database application that allows users to add, delete, update,
    and view movies along with their ratings and release years. Users can also view statistics about the movies,
    get a random movie recommendation, and search for movies by title."""
    action_list = {
        0 : ("Exit" ,exit_program),
        1 : ("List movies" ,show_all_movies_and_ratings),
        2 : ("Add movie" ,add_movie),
        3 : ("Delete movie" ,delete_movie),
        4 : ("Stats" ,show_stats),
        5 : ("Random movie" ,random_movie),
        6 : ("Search movie" ,search_movie),
        7 : ("Movies sorted by rating" ,show_sorted_movies),
        8 : ("Generate website" ,generate_website),
    }


    while True:
        print("******** My Movies Database **********\n")
        print("Menu:")
        print("Please choose an action by selecting a number (0-8):")

        for menu_key, action in action_list.items():
            print(f"{menu_key} : {action[0]}")

        try:
            user_input = int(input(
                "What do you wanna do? "
            ))
            action_list[user_input][1]()

        except KeyError:
            print("Unknown action. Please enter a valid action.")

        except ValueError:
            print("Please enter a number (0-8).")


if __name__ == "__main__":
    main()
