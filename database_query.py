import sqlite3

import resourses as res

def connect_database():
    global conn
    global cursor
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

def add_new_user(chat_id, name, topic):
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (
            chat_id,
            name,
            topic,
            res.Status.idle,
            '[]',
            '{}'
            ))
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        cursor.commit()

def search_user(chat_id):
    try:
        cursor.execute("SELECT * FROM users WHERE _chat_id == ?", (chat_id))
    except sqlite3.DatabaseError as err
        print("Error: ", err)
    else:
        return cursor.fetchall()

def get_all_topics():
    try:
        cursor.execute("SELECT DISTINCT _topic FROM words")
        topics = cursor.fetchall()
        return topics
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
