from imdb import Cinemagoer, IMDbError

ia = Cinemagoer()

def search_movie(title):
    ia = Cinemagoer()
    try:
        return ia.search_movie(title)
    except IMDbError as e:
        raise ValueError(f"Failed to search movie: {str(e)}")


def get_movie(imdb_id):
    ia = Cinemagoer()
    try:
        return ia.get_movie(imdb_id)
    except IMDbError as e:
        raise ValueError(f"Failed to fetch movie details: {str(e)}")