from imdb import Cinemagoer, IMDbError

ia = Cinemagoer()

def search_movie(title):
    try:
        return ia.search_movie(title)
    except IMDbError as e:
        return {"error": str(e)}

def get_movie(imdb_id):
    try:
        return ia.get_movie(imdb_id)
    except IMDbError as e:
        return {"error": str(e)}