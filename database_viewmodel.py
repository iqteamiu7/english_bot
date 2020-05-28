import json

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
    topics = db.get_all_topics()
    return topics

def change_user_selected_topic(chat_id, new_topic_name):
    pass

def get_unlearned_words(chat_id, max_word_count = 10):
    pass

def add_learned_words(chat_id, type_learning_words):
    pass

def get_learned_words(chat_id, max_word_count = 10):
    statistics = json.loads(db.get_user_statistics(chat_id)[0][0])
    topic = get_user_active_topic(chat_id)

    testing_words = res.type_testing_words.copy()
    if topic in statistics:
        for dictionary in statistics[topic]:
            if len(testing_words["testing_data"]) >= max_word_count:
                break

            item = res.type_testing_words_data.copy()
            item['ew'] = dictionary['ew']
            item['rw'] = dictionary['rw']

            testing_words["testing_data"].apped(item)

    return testing_words

def update_learned_words(chat_id, type_testing_words):
    words_data = type_testing_words["testing_data"]

    statistics = json.loads(db.get_user_statistics(chat_id)[0][0])
    topic = get_user_active_topic(chat_id)
    
    words_stat = statistics[topic]
    
    for word_data in words_data:
        for word_stat in words_stat:
            if word_data['ew'] == word_stat['ew']:
                if word_data['iactc'] == True:
                    word_stat['cact'] = int(word_stat['cact']) + 1
                    word_stat['aact'] = int(word_stat['aact']) + 1
                elif word_data['iactc'] == False:
                    word_stat['aact'] = int(word_stat['aact']) + 1
                break
    statistics[topic] = words_stat

    return True

def update_activity(chat_id, new_value):
    pass

def get_activity(chat_id):
    pass

def get_user_active_topic(chat_id):
    return db.get_user_active_topic(chat_id)[0][0]

if __name__ == "__main__":
    print("This is package file\n")
