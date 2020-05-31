import json
import copy

import database_query as db
import resourses as res

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
    init_emply_topic(chat_id)
    return True

def is_user_exists(chat_id):
    if db.search_user(chat_id) == []:
        return False
    return True

def delete_user(chat_id):
    if is_user_exists(chat_id) != True:
        return False
    db.delete_line(chat_id, 'users')
    if is_user_exists(chat_id):
        return False
    return True 

def change_user_status(chat_id, new_status):
    r = res.Status()
    if is_user_exists(chat_id) and new_status in r.get_status_types():
        db.change_user_status(chat_id, new_status)
        return True
    return False

def get_all_topics():
    topics = db.get_all_topics()
    res = [i[0] for i in topics]
    return res

def change_user_selected_topic(chat_id, new_topic_name):
    if is_user_exists(chat_id) and new_topic_name in get_all_topics():
        db.change_user_topic(chat_id, new_topic_name)
        init_emply_topic(chat_id)
        return True
    return False

def get_unlearned_words(chat_id, max_word_count = 5):
    statistics = json.loads(db.get_user_statistics(chat_id)[0][0])
    topic = get_user_active_topic(chat_id)
    all_topic_words = db.get_topic_words(topic)

    learned_words = []
    for i in range(len(statistics[topic])):
        learned_words.append(statistics[topic][i]['ew'])

    if topic in statistics:
        dictionary = []
        words_counter = 0
        for i in range(len(all_topic_words)):
            if len(dictionary) >= max_word_count:
                break
            if all_topic_words[i][0] not in learned_words:
                new_word = ([
                            ['ew', all_topic_words[i][0]],
                            ['rw', all_topic_words[i][1]],
                            ['il', 'None']
                            ])
                dictionary.append(dict(new_word))
                
        return dict([['current_index', 0],
                      ['learning_data', dictionary]]) 
    else:
        dictionary = []
        for i in range(max_word_count):
            new_word = ([
                    ['ew', all_topic_words[0]],
                    ['rw', all_topic_words[1]],
                    ['il', 'None']
                    ])
            dictionary.append(dict(new_word))
        return dict([['current_index', 0],
                      ['learning_data', dictionary]])

def add_learned_words(chat_id, learning_words):
    if not is_user_exists(chat_id):
        return False
    statistics = json.loads(db.get_user_statistics(chat_id)[0][0])
    topic = get_user_active_topic(chat_id)
    
    learned_words = statistics[topic]
    for word in learning_words['learning_data']:
        if word['il'] == True:
            del word['il']
            word.update(dict([['cact',0],['aact',0]]))
            learned_words.append(word)
    statistics[topic] = learned_words
    db.update_learned_words(chat_id, json.dumps(statistics))
    return True

def get_learned_words(chat_id, max_word_count = 100):
    statistics = json.loads(db.get_user_statistics(chat_id)[0][0])
    topic = get_user_active_topic(chat_id)
    
    testing_words = copy.deepcopy(res.type_testing_words)
    if topic in statistics:
        for dictionary in statistics[topic]:
            if len(testing_words["testing_data"]) >= max_word_count:
                break

            item = copy.deepcopy(res.type_testing_words_data)
            item['ew'] = dictionary['ew']
            item['rw'] = dictionary['rw']

            testing_words["testing_data"].append(item)

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
    str_stat = json.dumps(statistics)
    db.update_learned_words(chat_id, str_stat)

    return True

def get_user_statistics(chat_id):
    if is_user_exists(chat_id):
        stat = db.get_user_statistics(chat_id)[0][0]
        stat = json.loads(stat)

        return stat

def update_activity(chat_id, new_value):
    if is_user_exists(chat_id):
        db.change_user_activity(chat_id, new_value)
        return True
    else:
        return False

def get_activity(chat_id):
    activity = json.loads(db.get_user_activity(chat_id)[0][0])
    return activity

def get_user_active_topic(chat_id):
    return db.get_user_active_topic(chat_id)[0][0]

def init_emply_topic(chat_id):
    topic = get_user_active_topic(chat_id)
    statistics = json.loads(db.get_user_statistics(chat_id)[0][0])

    if topic in statistics:
        print("Topic inited already")
        return False

    statistics[topic] = []
    db.update_learned_words(chat_id, json.dumps(statistics))

def get_topic_size(topic):
    return db.get_num_of_words_in_topic(topic)

if __name__ == "__main__":
    print("This is package file\n")
