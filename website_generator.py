def load_html_template(movies):
    """Load the HTML template and replaces the placeholders with the HTML code."""
    html_code = generate_html(movies)
    with open("index_template.html", "r") as template:
        template_html = template.read()
        website_text_movies = template_html.replace("__TEMPLATE_MOVIE_GRID__", html_code)
        write_new_website(website_text_movies)


def generate_html(movies):
    """Generate the HTML code for the movies list."""
    output = ""
    for movie, information in movies.items():
        output += f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{information['picture']}">
                <div class="movie-title">{movie}</div>
                <div class="movie-year">{information['year']}</div>
            </div>
        </li>
        """

    return output


def write_new_website (html_code):
    """Creates new HTML page."""
    try:
        with open("index.html", "w") as website:
            website.write(html_code)
            print("Website was generated successfully.")
            input("Press Enter to continue...")

    except FileNotFoundError as err:
        print(f"Error: {err}")
