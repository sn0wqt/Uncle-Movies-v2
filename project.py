import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
from discord import app_commands
from reactionmenu import ViewMenu, ViewButton
from imdb import Cinemagoer, IMDbError


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


def load_data(filename="movies.json"):
    try:
        with open(filename, "r") as file:
            data = file.read().strip()
            if not data:
                return {"movies": []}
            return json.loads(data)
    except FileNotFoundError:
        return {"movies": []}
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in movies file")


def save_data(data, filename="movies.json"):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise IOError(f"Failed to save data to {filename}: {e}")


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


def create_movie_embed(movie, color):
    embed = discord.Embed(title=movie["title"], color=color)
    if movie.get("id"):
        embed.add_field(name="Movie ID", value=movie["id"], inline=True)
    embed.add_field(name="IMDb ID", value=movie["imdb_id"], inline=True)
    embed.add_field(name="Year", value=movie["year"], inline=True)
    embed.add_field(name="Rating", value=movie.get("rating", "N/A"), inline=True)

    if movie.get("user_rating"):
        embed.add_field(name="User Rating", value=movie["user_rating"], inline=True)
    if movie.get("plot_outline"):
        embed.add_field(name="Plot Outline", value=movie["plot_outline"], inline=False)

    if cover_url := movie.get("cover_url", ""):
        if cover_url.startswith(("http", "https")):
            embed.set_image(url=cover_url)
    else:
        embed.add_field(name="Cover URL", value="No cover available", inline=False)

    return embed


def setup_bot(bot):
    @bot.event
    async def on_ready():
        print("Uncle Movie is up and running...")

        activity = discord.Activity(
            type=discord.ActivityType.watching, name="the movie list 🍿"
        )
        await bot.change_presence(activity=activity)

        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(f"Error syncing commands: {e}")

    @bot.tree.command(name="ping", description="Check if the bot is responsive")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @bot.tree.command(name="list", description="List all movies in your collection.")
    async def list(interaction: discord.Interaction):
        movies = get_movie_list()
        if not movies:
            await interaction.response.send_message("No movies found.")
            return

        menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed)
        for movie in movies:
            menu.add_page(create_movie_embed(movie, discord.Color.pink()))

        menu.add_button(ViewButton.back())
        menu.add_button(ViewButton.next())
        await menu.start()

    @bot.tree.command(name="search", description="Search for a movie by title.")
    @app_commands.describe(title="The title of the movie to search for")
    async def search(interaction: discord.Interaction, title: str):
        try:
            await interaction.response.defer()

            movies = search_movies(title)
            if not movies:
                await interaction.followup.send("No results found.")
                return

            menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed)
            for movie in movies:
                menu.add_page(create_movie_embed(movie, discord.Color.green()))

            menu.add_button(ViewButton.back())
            menu.add_button(ViewButton.next())
            await menu.start()
        except ValueError as e:
            await interaction.followup.send(str(e))

    @bot.tree.command(
        name="add", description="Add a movie to the list using its IMDB ID"
    )
    @app_commands.describe(imdb_id="The IMDB ID of the movie")
    async def add(interaction: discord.Interaction, imdb_id: str):
        try:
            await interaction.response.defer()
            response = add_movie(imdb_id)
            await interaction.followup.send(response)
        except ValueError as e:
            await interaction.followup.send(str(e))

    @bot.tree.command(name="delete", description="Delete a movie from the list by ID")
    @app_commands.describe(id="The database ID of the movie to delete")
    async def delete(interaction: discord.Interaction, id: int):
        try:
            response = delete_movie(id)
            await interaction.response.send_message(response)
        except ValueError as e:
            await interaction.response.send_message(str(e))

    @bot.tree.command(name="rate", description="Rate a movie in your collection.")
    @app_commands.describe(
        id="The movie ID to rate", user_rating="Your rating out of 10"
    )
    async def rate(interaction: discord.Interaction, id: int, user_rating: int):
        try:
            response = rate_movie(id, user_rating)
            await interaction.response.send_message(response)
        except ValueError as e:
            await interaction.response.send_message(str(e))

    @bot.tree.command(
        name="help",
        description="Get a list of all available commands and how to use them.",
    )
    async def help(interaction: discord.Interaction):
        embed = discord.Embed(
            title="Uncle Movies Bot - Command Help",
            description="Here is a list of commands and how to use them.",
            color=discord.Color.blue(),
        )

        embed.add_field(
            name="/search <title>",
            value=(
                "Search for a movie or TV series by title. "
                "The results will show the movie details along with the IMDb ID.\n"
                "**Example:** `/search Shawshank Redemption`\n"
                "You can copy the IMDb ID from the search results."
            ),
            inline=False,
        )

        embed.add_field(
            name="/add <imdb_id>",
            value=(
                "Add a movie to your collection using its IMDb ID.\n"
                "**Example:** `/add 0417299`\n"
                "You can get the IMDb ID from the `/search` command."
            ),
            inline=False,
        )

        embed.add_field(
            name="/list",
            value="List all movies in your collection with full details.",
            inline=False,
        )

        embed.add_field(
            name="/rate <id> <rating>",
            value=(
                "Rate a movie in your collection by providing its ID and your rating out of 10.\n"
                "**Example:** `/rate 5 9`\n"
                "Use `/list` to find the movie ID."
            ),
            inline=False,
        )

        embed.add_field(
            name="/delete <id>",
            value=(
                "Remove a movie from your collection by providing its ID.\n"
                "**Example:** `/delete 3`\n"
                "Use `/list` to find the movie ID."
            ),
            inline=False,
        )

        embed.add_field(
            name="/ping",
            value="Check if the bot is online and responsive.",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)


def main():
    try:
        load_dotenv()
    except FileNotFoundError:
        print("No .env file found")

    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    setup_bot(bot)

    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("Missing BOT_TOKEN in .env")

    bot.run(bot_token)


if __name__ == "__main__":
    main()
