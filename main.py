import telebot

import database_viewmodel as db_vm
import command
import learning
import testing
from resourses import Emoji
import main_model as m_m
#PLEASE INSERT YOUR TOKEN HERE
m_m.bot = telebot.TeleBot(TOKEN)

db_vm.connect_database()


@m_m.bot.callback_query_handler(func=lambda query: True)
def callback_query_topic(query):
    topic = query.data[:query.data.index('_')]
    user_id = command.get_user_id_from_query(query)

    db_vm.change_user_selected_topic(user_id, topic)
    m_m.bot.answer_callback_query(query.id, "Тема сменена на " + topic)

@m_m.bot.message_handler(commands=['start', 'help', 'hide', 'show',
        'delete_me', 'stop_testing'])
def commands_listener(message):
    chat_id = message.chat.id
    if not db_vm.is_user_exists(chat_id) and message.text != "/start":
        m_m.bot.send_message(chat_id, "Register first\n/start")
        return

    if message.text.find("/start") == 0:
        command.on_start(message)
    elif message.text.find("/help") == 0:
        command.on_help(chat_id)
    elif message.text.find("/hide") == 0:
        m_m.Menu.hide(chat_id)
    elif message.text.find("/show") == 0:
        m_m.Menu.show_main(chat_id)
    elif message.text.find("/delete_me") == 0:
        command.on_delete_me(chat_id)
    elif message.text.find("/stop_testing") == 0:
        m_m.bot.reply_to(message, "This command words only during testing")

@m_m.bot.message_handler(func = lambda m: True)
def menu_buttons_listener(message):
    chat_id = message.chat.id
    if not db_vm.is_user_exists(chat_id):
        m_m.bot.send_message(chat_id, "Register first\n/start")
        return


    # Main menu
    if message.text == m_m.Menu._learn:
        learning.start_learning(message)
    elif message.text == m_m.Menu._test:
        m_m.Menu.show_tests(chat_id)
    elif message.text == m_m.Menu._topic:
        command.on_topic_change(chat_id)
    elif message.text == m_m.Menu._statistics:
        command.on_show_statistics(chat_id)


    # Test menu
    elif message.text == m_m.Menu._active_test:
        testing.start_testing(message)
    elif message.text == m_m.Menu._go_to_main_menu:
        m_m.Menu.show_main(chat_id)

    else:
        m_m.bot.send_message(chat_id, "Hmmmm... I don\'t understand")

m_m.bot.enable_save_next_step_handlers(delay=2)
m_m.bot.load_next_step_handlers()
m_m.bot.polling()
