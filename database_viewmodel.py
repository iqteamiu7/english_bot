import database_query as db

def connect_database():
    db.connect_database()

def add_new_user(chat_id, name):
    '''Add a new user to database by chat_id

    Return
    ------
    False
        If user exists
    True
        If user added
    '''
    if is_user_exists(chat_id):
        return False

    topic = get_all_topics()[0]
    db.add_new_user(chat_id, name, topic)
    return True

def is_user_exists(chat_id):
    if db.search_user == []:
        return False
    return True

def delete_user(chat_id):
    pass

def change_user_status(chat_id, new_status):
    pass

def get_all_topics():
    pass

def change_user_selected_topic(chat_id, new_topic_name):
    pass

def get_unlearned_words(chat_id, max_word_count = 10):
    pass

def add_learned_words(chat_id, type_learning_words):
    pass

def get_learned_words(chat_id, max_word_count = 10):
    pass

def update_learned_words(chat_id, type_testing_words):
    pass

def update_activity(chat_id, new_value):
    pass

def get_activity(chat_id):
    pass

if __name__ == "__main__":
    print("This is package file\n")
