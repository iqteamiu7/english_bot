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
            '{}',
            '{}'
            ))
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()

def search_user(chat_id):
    try:
        cursor.execute("SELECT * FROM users WHERE _chat_id == ?", (chat_id,))
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        return cursor.fetchall()

def get_user_statistics(chat_id):
    try:
        cursor.execute("SELECT _statistics FROM users WHERE _chat_id == ?",
                (chat_id,))
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        return cursor.fetchall()

def get_user_active_topic(chat_id):
    try:
        cursor.execute("SELECT _active_topic FROM users WHERE _chat_id == ?",
                (chat_id,))
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        return cursor.fetchall()

def update_learned_words(chat_id, new_value):
    try:
        cursor.execute("UPDATE users SET _statistics = ? WHERE _chat_id == ?",
                (new_value, chat_id))
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()

def get_all_topics():
    try:
        cursor.execute("SELECT DISTINCT _topic FROM words")
        topics = cursor.fetchall()
        return topics
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

def delete_line(chat_id, table):
    try:
        if table == 'users':
            cursor.execute("DELETE FROM users WHERE _chat_id = ?", (chat_id,))
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()

def change_user_topic(chat_id, topic_name):
    try:
        cursor.execute("UPDATE users SET _active_topic = ? WHERE _chat_id = ?", (
            topic_name,
            chat_id))
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()
