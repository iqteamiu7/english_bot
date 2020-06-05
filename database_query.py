import sqlite3

import resourses as res

def connect_database():
    global conn
    global cursor
    conn = sqlite3.connect("database.db", check_same_thread = False)
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

def get_user_status(chat_id):
    try:
        cursor.execute("SELECT _status FROM users WHERE _chat_id == ?",
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
        cursor.execute("UPDATE users SET _active_topic = ? WHERE _chat_id = ?",
                (topic_name, chat_id))
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()

def change_user_status(chat_id, new_status):
    try:
        cursor.execute("UPDATE users SET _status = ? WHERE _chat_id = ?", (
            new_status,
            chat_id))
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()

def get_topic_words(topic_name):
    try:
        cursor.execute(
                "SELECT _eng_word, _ru_word FROM words WHERE _topic = ?",
                (topic_name,))
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
        return []
    else:
        return cursor.fetchall()

def get_num_of_words_in_topic(topic):
    cursor.execute(f"select count(*) from words where _topic = '{topic}'")
    return cursor.fetchall()

if __name__ == "__main__":
    print("This is package file\n")
