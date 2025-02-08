# Uncle Movies Bot
#### Video Demo:
#### Description:

The **Uncle Movies Bot** is a **Discord bot** built to make managing your favorite movies and TV shows effortless. It taps into the IMDb database with the help of the `cinemagoer` library (the continued version of the old `imdbpy`), so you can quickly pull movie details right in Discord. Keep track of your movie collection, add your own ratings, and get all the juicy details neatly presented.

---

### **Features**

- **Search Movies:**
    Use the `/search` command to look up movies or TV series by title. You'll see key details like the title, IMDb ID, release year, and even a cover image.

- **Add Movie to Collection:**
    Add a movie to your personal collection with the `/add` command by entering its IMDb ID. The bot checks for duplicates so you don't end up with the same movie twice.

- **List Movies:**
    The `/list` command shows all the movies in your collection. Each entry comes with the title, cover image, release year, IMDb rating, your custom rating, and a plot outline.

- **Rate a Movie:**
    With the `/rate` command, you can rate movies in your collection, then compare your rating to the IMDb one.

- **Delete Movie:**
    Remove a movie from your collection using the `/delete` command by providing the movie's ID.

- **Help Command:**
    The `/help` command gives a quick rundown of all available commands along with their usage examples.

- **Ping Command:**
    Use `/ping` to quickly check if the bot is online.

---

### **Project Structure**

The project is written in Python and leverages libraries like **discord.py**, **reactionmenu**, and **cinemagoer**. Here’s a quick look at the files:

1. **project.py**
     This file handles all the bot's main functions, including searching, adding, listing, rating, and deleting movies. It also takes care of Discord events like when the bot comes online (`on_ready`) and processes command interactions. Notable functions include:
     - `add_movie()`: Adds a movie to your collection.
     - `delete_movie()`: Removes a movie using its ID.
     - `rate_movie()`: Updates your movie rating.
     - `get_movie_list()`: Fetches your movie list from `movies.json`.
     - `search_movies()`: Gets search results from IMDb.
     - `create_movie_embed()`: Makes a neat embed to show movie details on Discord.

2. **movies.json**
     This JSON file keeps a record of your movie collection, storing details like title, IMDb ID, release year, ratings, cover image, and plot.

3. **.env**
     The `.env` file holds sensitive info such as your bot token needed for Discord authentication.

4. **test_project.py**
     Contains test cases to ensure everything works correctly—from handling duplicates to updating ratings.

---

### **Design Choices**

1. **Project Structure:**
     Initially, features and API calls were split into separate files for clarity. But following the CS50P project guidelines (which specify having just one `project.py` file), everything was consolidated into one file.

2. **Data Storage:**
     I opted for a JSON file (`movies.json`) to keep the project lightweight and easy to manage. While a database might be ideal for scaling, JSON works well for this project's scope.

3. **Embed Display:**
     Instead of plain text dumps, rich embeds are used to display movie info. This makes it visually engaging and easy to navigate.

4. **Command Design:**
     The shift from old prefix commands (like `!ping` or `?help`) to slash commands (e.g. `/ping`, `/help`) offers a smoother, more user-friendly experience. Discord’s built-in autocomplete and formatting improve usability and reduce the need to remember complicated commands.

---

### **Future Improvements**

- **Advanced Search Filters:**
    Introduce filters like genre, year, or rating so users can quickly find movies that match their preferences.

- **Role-Based Permissions:**
    Limit commands like `/delete` to certain users to prevent accidental removals—nobody wants their entire collection wiped out by a well-meaning friend.

- **Database Integration:**
    Switching from JSON to a full database solution would help manage a larger movie collection more efficiently.

- **Error Logging:**
    Implement proper logging so that any issues are tracked instead of the bot quietly hoping nobody notices when something goes wrong.

- **User/Group Specific Lists:**
    Add the option for a separate movie list per user or group, ensuring personalized collections so that movie entries don't overlap.

---

### How to Run the Project


1. **Clone the Repository**
   - Open your terminal and run:
     ```bash
     git clone <your-repository-url>
     cd <repository-folder>
     ```


2. **Install Dependencies**
   - Run:
     ```bash
     pip install -r requirements.txt
     ```


3. **Configure Environment Variables**
   - Create a `.env` file in the project root and add your bot token:
     ```env
     BOT_TOKEN="<Your_Discord_Bot_Token>"
     ```
   - Make sure the token is within quotation marks `""`


4. **Verify Python Version**
   - Ensure you have **Python 3.7+** installed.
   - Confirm necessary permissions to run the bot on your Discord server.


5. **Start the Bot**
   - Launch it with:
     ```
     python project.py
     ```


6. **Invite the Bot to Your Discord Server**
   - Visit the [Discord Developer Portal](https://discord.com/developers/applications) and select your bot.
   - Generate an **OAuth2 URL** by:
     - Choosing the **bot** and **application.commands** scopes.
     - Assigning required permissions (e.g., *Send Messages* and *Embed Links*).
   - Copy the URL and invite the bot to your server.


7. **Get Started with Commands**
   - Once online, type `/help` in your Discord server to view available commands.


8. **Stop the Bot**
   - Press **Ctrl+C** in your terminal.
   - Alternatively, stop the process manually.
