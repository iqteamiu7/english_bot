import main_model as m_m
from resourses import Emoji
import database_viewmodel as db_vm
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def on_start(message):
    chat_id = message.chat.id

    if db_vm.is_user_exists(chat_id):
        m_m.bot.send_message(chat_id, "You are already registered")
        return False

    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    if first_name == None: first_name = "stranger"
    if last_name == None: last_name = ""
    full_name = first_name + " " + last_name

    m_m.bot.send_message(chat_id, "Hello, " + first_name + ' ' + Emoji.hello)
    m_m.bot.send_message(chat_id, "I will help you learn words in English " +
            Emoji.tea_cap)
    markup = m_m.Menu.get_main_markup()
    m_m.bot.send_message(chat_id, "We will communicate using the buttons" +
            Emoji.finger_down, reply_markup = markup)

    db_vm.add_new_user(chat_id, full_name)
    return True

def gen_inline_markup(page, user_id):
    topics = db_vm.get_all_topics()
    ROW_WIDTH = 4
    inline_markup = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    for i in topics[page * ROW_WIDTH:(page * ROW_WIDTH) + ROW_WIDTH]:
        inline_markup.row(InlineKeyboardButton(i, callback_data=i + '_' + str(user_id)))
    return inline_markup

def on_help(chat_id):
    # TODO: come up with a useful message
    m_m.bot.send_message(chat_id, "Unhelpful message\n¯\_(ツ)_/¯")

def on_delete_me(chat_id):
    m_m.bot.send_message(chat_id, "Let's try to delete you")
    if db_vm.delete_user(chat_id):
        m_m.bot.send_message(chat_id, "Success")
        return False

    m_m.bot.send_message(chat_id, "Fail")
    return True

def on_show_statistics(chat_id):
    active_topic = db_vm.get_user_active_topic(chat_id)
    stat = db_vm.get_user_statistics(chat_id)
    count_words = len([i for i in stat[active_topic]])
    num_of_words = db_vm.get_topic_size(active_topic)
    del stat[active_topic]

    msg = \
        "Current topic: %s %s\n\
Number of words in topic: %d \n\
Number of learned words in topic: %d\n" % (active_topic.capitalize(),
        Emoji.topic_to_emoji[active_topic], num_of_words, count_words)
    stat_msg = [msg]
    for topic in stat.items():
        count_words = len([i for i in topic[1]])
        num_of_words = db_vm.get_topic_size(topic[0])
        msg = \
                "Topic: %s %s\n\
Number of words in topic: %d \n\
Number of learned words in topic: %d\n" % (topic[0].capitalize(),
        Emoji.topic_to_emoji[topic[0]], num_of_words, count_words)
        stat_msg.append(msg)

    for topic in stat_msg:
        m_m.bot.send_message(chat_id, topic)

def on_topic_change(chat_id):
    if db_vm.get_user_status(chat_id) == 'idle':
        m_m.bot.send_message(chat_id, "Выберите тему", 
                reply_markup=gen_inline_markup(0, chat_id))

def get_user_id_from_query(query):
    return int(query.data[query.data.index('_') + 1:])

if __name__ == "__main__":
    print("This is package file\n")
