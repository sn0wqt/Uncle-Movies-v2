# Uncle Movies Bot  
#### Video Demo: [Insert URL here]  
#### Description:  

The **Uncle Movies Bot** is a **Discord bot** designed to help users **log, search, manage, and rate** their favorite movies and TV series. It features a seamless integration with the IMDb database using the `cinemagoer` library (the continuation of the now-deprecated `imdbpy` library), allowing users to search for movie details directly from Discord. Users can maintain a collection of movies, add custom ratings, and view detailed information about each entry, presented in visually rich embeds for a clean and organized experience.

---

### **Features**

- **Search Movies:**  
  Users can search for movies or TV series by title using the `/search` command. Results include essential details like the title, IMDb ID, release year, IMDb rating, and cover image.  
   
- **Add Movie to Collection:**  
  The `/add` command allows users to add a movie to their personal collection by providing the IMDb ID. The bot checks if the movie already exists in the collection to prevent duplicates.

- **List Movies:**  
  The `/list` command displays all movies in the user's collection. Each movie is shown with full details, including the title, release year, IMDb rating, custom user rating, and plot outline.

- **Rate a Movie:**  
  Users can rate a movie in their collection using the `/rate` command. The bot saves the user rating, allowing them to compare it with the IMDb rating.

- **Delete Movie:**  
  The `/delete` command allows users to remove a movie from their collection using the movie's ID.

- **Help Command:**  
  The `/help` command provides users with an overview of all available commands, their syntax, and example usage.

- **Ping Command:**  
  A simple `/ping` command to check if the bot is responsive.

---

### **Project Structure**

The project is implemented in Python and uses several libraries, including **discord.py**, **reactionmenu**, and **cinemagoer**. Here's an overview of the files in the project:

1. **project.py**  
   This file contains all the bot's core functionality. It defines commands for searching, adding, listing, rating, and deleting movies. It also handles Discord events such as bot startup (`on_ready`) and command interactions. Key functions include:
   - `add_movie()`: Adds a movie to the collection if it does not already exist.
   - `delete_movie()`: Removes a movie from the collection based on its ID.
   - `rate_movie()`: Updates the user rating for a specific movie.
   - `get_movie_list()`: Retrieves the list of movies from the `movies.json` file.
   - `search_movies()`: Fetches search results from IMDb for a given title.
   - `create_movie_embed()`: Generates a rich embed to display movie details on Discord.

2. **movies.json**  
   This JSON file stores the user's movie collection, including details like title, IMDb ID, release year, ratings, and plot outlines.

3. **requirements.txt**  
   This file lists the Python dependencies required to run the project. Major libraries include:
   - `discord.py`: For interacting with the Discord API.
   - `reactionmenu`: For creating menu-based embeds.
   - `cinemagoer`: For fetching movie data from IMDb.
   - `python-dotenv`: For loading environment variables from a `.env` file.

4. **.env**  
   The `.env` file (not included in public repositories) stores sensitive information like the bot token, which is necessary for authenticating the bot with Discord.

5. **test_project.py**  
   This file includes test cases to ensure the bot's core functions work as expected. Tests cover various scenarios such as adding duplicate movies, deleting non-existent movies, and updating user ratings.

---

### **Design Choices**

1. **Initial Project Structure:**  
   Initially, I separated core features, data handling, and API calls into separate files for better modularity. The bot commands were also placed in a separate file. However, after reading the project guidelines on CS50P, which specified that all code should be contained in `project.py`, I combined everything into a single file as required by the course.

2. **Error Handling Approach:**  
   I used **dictionary-based error handling** for simplicity. Each function returns either a success message or an error message in a consistent format, allowing the commands to handle responses easily.

3. **Data Storage:**  
   I chose to store movie data in a JSON file (`movies.json`) to keep the project lightweight and simple. While a database would offer better scalability, JSON is sufficient for this project's current scope.

4. **Embed Display Design:**  
   Instead of dumping raw text, I opted to use rich embeds to present movie information. This makes the output visually appealing and easier to navigate.

5. **Command Design:**  
   Each command was designed to provide clear and concise interactions. For example, the `/add` and `/delete` commands provide direct feedback on whether the operation was successful or encountered an error.

---

### **Future Improvements**

- **Advanced Search Filters:**  
  Implementing filters such as genre, year, or rating to refine search results.

- **Role-Based Permissions:**  
  Restricting certain commands (e.g., `/delete`) to authorized users or roles.

- **Database Integration:**  
  Migrating from JSON to a database for better scalability and performance.

- **Error Logging:**  
  Adding logging to capture and debug errors more efficiently.

---

### **How to Run the Project**

1. **Clone the Repository**
    - Open your terminal and run:
      ```
      git clone <your-repository-url>
      cd <repository-folder>
      ```

2. **Install Dependencies**
    - Install the required dependencies with:
      ```
      pip install -r requirements.txt
      ```

3. **Configure Environment Variables**
    - Create a `.env` file in the project's root directory and add your bot token:
      ```
      BOT_TOKEN=<Your_Discord_Bot_Token>
      ```
        - `<Your_Discord_Bot_Token>` should be inside quotations `""`

4. **Verify Python Version**
    - Ensure you have **Python 3.7+** installed and that you have the necessary permissions to run the bot on your Discord server.

5. **Start the Bot**
    - Launch the bot by executing:
      ```
      python project.py
      ```

6. **Invite the Bot to Your Discord Server**
    - Go to the [Discord Developer Portal](https://discord.com/developers/applications) and navigate to your bot.
    - Generate an **OAuth2 URL** by:
      - Selecting the **bot** and **application.commands** scopes under OAuth2 settings.
      - Assigning the required permissions (e.g., Send Messages, Embed Links).
    - Copy the generated URL and use it to invite the bot to your server.

7. **Get Started with Commands**
    - Once the bot is online, use the `/help` command on your Discord server to view all available commands.

8. **Stop the Bot**
    - Terminate the running bot by pressing **Ctrl+C** in your terminal or manually stopping the process.
