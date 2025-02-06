# import re
# import discord
# import os
# from discord import app_commands
# from discord.ext import commands
# from dotenv import load_dotenv
# import asyncio
# import json
# import uuid
from imdb import Cinemagoer

ia = Cinemagoer()

# from search movies, pick id and use it get name, year, rating, director, plot and genre
movies = ia.search_movie("Avatar")
for movie in movies:
    print(movie['title'])
    print(movie['year'])
    print(movie['cover url'])

def main(): ...

def search_movie(title):
    movie = ia.search_movie(title)
    return movie

def get_movie_details(movie_id):
    movie = ia.get_movie(movie_id)
    return movie


# def function_1(): ...


# def function_2(): ...


# def function_n(): ...


# if __name__ == "__main__":
#     main()