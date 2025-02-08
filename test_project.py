from project import load_data, save_data, add_movie, delete_movie, rate_movie, get_movie_list, search_movies


def reset_movies_file():
    initial_data = {
        "movies": [
            {
                "id": 1,
                "imdb_id": "0417299",
                "title": "Avatar: The Last Airbender",
                "year": 2005,
                "cover_url": "https://m.media-amazon.com/images/M/MV5BMDMwMThjYWYtY2Q2OS00OGM2LTlkODQtNDJlZTZmMjAyYmFhXkEyXkFqcGc@.jpg",
                "rating": 9.3,
                "user_rating": None,
                "plot_outline": (
                    "The world is divided into four elemental nations: The Northern "
                    "and Southern Water Tribes, the Earth Kingdom, the Fire Nation, and the Air Nomads. "
                    "The Avatar upholds the balance between the nations, but everything changed when the "
                    "Fire Nation invaded. Only the Avatar, master of all four elements, can stop them. But "
                    "when the world needs him most, he vanishes. A hundred years later Katara and Sokka "
                    "discover the new Avatar, an airbender named Aang. Together they must help Aang master "
                    "the elements and save the world."
                ),
            }
        ]
    }
    save_data(initial_data)


def test_load_data():
    reset_movies_file()
    data = load_data()
    assert isinstance(data, dict)
    assert "movies" in data
    assert len(data["movies"]) == 1


def test_save_data():
    reset_movies_file()
    data = load_data()
    data["movies"].append({"id": 2, "title": "Test Movie"})
    save_data(data)

    loaded_data = load_data()
    assert len(loaded_data["movies"]) == 2


def test_add_movie():
    reset_movies_file()
    result = add_movie("0111161")
    assert "message" in result
    assert "successfully added" in result["message"]

    data = load_data()
    assert len(data["movies"]) == 2

    result = add_movie("0111161")
    assert "error" in result
    assert result["error"] == "movie already exists"


def test_delete_movie():
    reset_movies_file()
    movie_id = 1

    result = delete_movie(movie_id)
    assert "message" in result
    assert "successfully deleted" in result["message"]

    data = load_data()
    assert not any(movie["id"] == movie_id for movie in data["movies"])

    result = delete_movie(movie_id)
    assert "error" in result
    assert result["error"] == "Movie not found"


def test_rate_movie():
    reset_movies_file()
    movie_id = 1

    result = rate_movie(movie_id, 9)
    assert "message" in result
    assert "User rating updated" in result["message"]

    data = load_data()
    rated_movie = next((m for m in data["movies"] if m["id"] == movie_id), None)
    assert rated_movie is not None
    assert rated_movie["user_rating"] == 9

    result = rate_movie(9999, 8)
    assert "error" in result
    assert result["error"] == "Movie not found"


def test_get_movie_list():
    reset_movies_file()
    movies = get_movie_list()
    assert isinstance(movies, list)
    assert len(movies) == 1
    assert movies[0]["title"] == "Avatar: The Last Airbender"


def test_search_movies():
    result = search_movies("The Shawshank Redemption")
    assert isinstance(result, list)
    assert len(result) > 0

    movie = result[0]
    assert "imdb_id" in movie
    assert "title" in movie
