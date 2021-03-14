import sqlite3
import csv
import os

conn = sqlite3.connect("database.db")
curr = conn.cursor()

table_names = ["transactions", "users", "emotions", "songs"]
for table in table_names:
    curr.execute(f"DROP TABLE IF EXISTS {table}")

# Sets up the database tables
curr.execute(
    """
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER NOT NULL,
        emotion_id INTEGER NOT NULL,
        song_link TEXT NOT NULL
    )
    """
)

curr.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
    )
    """
)

curr.execute(
    """
    CREATE TABLE IF NOT EXISTS emotions (
        emotion_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        emotion TEXT NOT NULL
    )
    """
)


# Set up users
curr.executescript(
    """
    INSERT INTO users (first_name, last_name) VALUES ("Jed", "Magracia");
    INSERT INTO users (first_name, last_name) VALUES ("Neelima", "Jyothiraj");
    INSERT INTO users (first_name, last_name) VALUES ("Alexa", "Urrea");
    """
)

# Set up users
curr.executescript(
    """
    INSERT INTO emotions (emotion) VALUES ("happy");
    INSERT INTO emotions (emotion) VALUES ("sad");
    INSERT INTO emotions (emotion) VALUES ("neutral");
    INSERT INTO emotions (emotion) VALUES ("surprised");
    INSERT INTO emotions (emotion) VALUES ("angry");
    """
)

cwd = os.getcwd()
csv_files = os.listdir(os.path.join(cwd,"songs"))
for csv_file in csv_files:
    user = csv_file.strip("_songs.csv")
    with open("songs/" + csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            emotion = row[0]
            link = row[1]

            curr.execute("SELECT user_id FROM users WHERE first_name=?", (user,))
            user_id = int(curr.fetchone()[0])

            curr.execute("SELECT emotion_id FROM emotions WHERE emotion=?", (emotion,))
            emotion_id = int(curr.fetchone()[0])

            curr.execute("INSERT INTO transactions (user_id, emotion_id, song_link) VALUES (?, ?, ?)", (user_id, emotion_id, link))

conn.commit()
conn.close()