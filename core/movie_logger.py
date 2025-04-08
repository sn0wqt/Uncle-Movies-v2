from .data_handler import load_data, save_data
from .movie import search_movie, get_movie


def get_movie_list():
    return load_data().get("movies", [])


def search_movies(title):
    search_results = search_movie(title)
    if "error" in search_results:
        raise ValueError(search_results["error"])

    movie_list = []
    for movie in search_results:
        movie_list.append(
            {
                "imdb_id": movie.getID(),
                "title": movie.get("title"),
                "year": movie.get("year", "N/A"),
                "cover_url": movie.get("full-size cover url", "N/A"),
            }
        )
    return movie_list


def add_movie(imdb_id):
    data = load_data()

    if imdb_id in [movie["imdb_id"] for movie in data["movies"]]:
        raise ValueError("Movie already exists")

    selected = get_movie(imdb_id)
    if "error" in selected:
        raise ValueError(selected["error"])

    id = max((movie["id"] for movie in data["movies"]), default=0) + 1

    movie = {
        "id": id,
        "imdb_id": imdb_id,
        "title": selected.get("title"),
        "year": selected.get("year", "N/A"),
        "cover_url": selected.get("full-size cover url", "N/A"),
        "rating": selected.get("rating", "N/A"),
        "user_rating": None,
        "plot_outline": selected.get("plot outline", "N/A"),
    }

    data["movies"].append(movie)
    save_data(data)
    return f"{movie['title']} successfully added"


def delete_movie(id):
    data = load_data()
    for movie in data["movies"]:
        if movie["id"] == id:
            data["movies"].remove(movie)
            save_data(data)
            return f"{movie['title']} successfully deleted"
    raise ValueError("Movie not found")


def rate_movie(id, user_rating):
    data = load_data()
    for movie in data["movies"]:
        if movie["id"] == id:
            movie["user_rating"] = user_rating
            save_data(data)
            return f"User rating updated for {movie['title']}"
    raise ValueError("Movie not found")
