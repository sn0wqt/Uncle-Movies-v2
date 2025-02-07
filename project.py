import discord
from discord.ext import commands
from dotenv import load_dotenv
from commands import setup_bot
import os


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
