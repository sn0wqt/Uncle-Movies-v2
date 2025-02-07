import discord
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from reactionmenu import ViewMenu, ViewButton
from movie_logger import (
    get_movie_list,
    search_movies,
    add_movie,
    rate_movie,
    delete_movie,
)

try:
    load_dotenv()
except FileNotFoundError:
    print("No .env file found")

bot_token = os.getenv("BOT_TOKEN")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Uncle Movie is up and running...")
    
    activity = discord.Activity(type=discord.ActivityType.watching, name="the movie list 🍿")
    await bot.change_presence(activity=activity)

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


@bot.tree.command(name="ping", description="Check if the bot is responsive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


@bot.tree.command(name="search", description="Search for a movie by title.")
@app_commands.describe(title="The title of the movie to search for")
async def search(interaction: discord.Interaction, title: str):
    movies = search_movies(title)
    if "error" in movies:
        await interaction.response.send_message(movies["error"])
        return

    menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed)

    for movie in movies:
        embed = discord.Embed(title=movie["title"], color=discord.Color.green())
        embed.add_field(name="Year", value=movie["year"], inline=True)
        embed.add_field(name="IMDb ID", value=movie["imdb_id"], inline=True)
        embed.add_field(name="Rating", value=movie.get("rating", "N/A"), inline=True)
        embed.add_field(
            name="Plot Outline", value=movie.get("plot_outline", "N/A"), inline=False
        )

        cover_url = movie.get("cover_url", "")
        if cover_url and (
            cover_url.startswith("http") or cover_url.startswith("https")
        ):
            embed.set_image(url=cover_url)
        else:
            embed.set_footer(text="Cover image not available.")

        menu.add_page(embed)

    menu.add_button(ViewButton.back())
    menu.add_button(ViewButton.next())

    await menu.start()


@bot.tree.command(name="add", description="Add a movie to the list using its IMDB ID")
@app_commands.describe(imdb_id="The IMDB ID of the movie")
async def add(interaction: discord.Interaction, imdb_id: str):
    await interaction.response.defer()
    result = add_movie(imdb_id)
    if "message" in result:
        await interaction.followup.send(result["message"])
    else:
        await interaction.followup.send(result["error"])
        
        
@bot.tree.command(name="delete", description="Delete a movie from the list by ID")
@app_commands.describe(id="The database ID of the movie to delete")
async def delete(interaction: discord.Interaction, id: int):
    result = delete_movie(id)
    if "message" in result:
        await interaction.response.send_message(result["message"])
    else:
        await interaction.response.send_message(result["error"])


@bot.tree.command(name="rate", description="Rate a movie in your collection.")
@app_commands.describe(id="The movie ID to rate", user_rating="Your rating out of 10")
async def rate(interaction: discord.Interaction, id: int, user_rating: int):
    result = rate_movie(id, user_rating)

    if "message" in result:
        await interaction.response.send_message(result["message"])
    else:
        await interaction.response.send_message(result["error"])


@bot.tree.command(name="list", description="List all movies in your collection.")
async def list(interaction: discord.Interaction):
    movies = get_movie_list()
    if not movies:
        await interaction.response.send_message("No movies found.")
        return

    menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed)

    for movie in movies:
        embed = discord.Embed(title=movie["title"], color=discord.Color.blue())
        embed.add_field(name="Movie ID", value=movie["id"], inline=True)
        embed.add_field(name="Year", value=movie["year"], inline=True)
        embed.add_field(name="IMDb ID", value=movie["imdb_id"], inline=True)
        embed.add_field(
            name="IMDb Rating", value=movie.get("rating", "N/A"), inline=True
        )
        embed.add_field(
            name="User Rating", value=movie.get("user_rating", "N/A"), inline=True
        )
        embed.add_field(
            name="Plot Outline", value=movie.get("plot_outline", "N/A"), inline=False
        )

        cover_url = movie.get("cover_url", "")
        if cover_url and (
            cover_url.startswith("http") or cover_url.startswith("https")
        ):
            embed.set_image(url=cover_url)
        else:
            embed.set_footer(text="Cover image not available.")

        menu.add_page(embed)

    menu.add_button(ViewButton.back())
    menu.add_button(ViewButton.next())

    await menu.start()


@bot.tree.command(
    name="help", description="Get a list of all available commands and how to use them."
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
        name="/ping", value="Check if the bot is online and responsive.", inline=False
    )

    await interaction.response.send_message(embed=embed)


bot.run(bot_token)
