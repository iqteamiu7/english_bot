import telebot

import database_viewmodel as db_vm
import command
import learning
import testing
from resourses import Emoji
import main_model as m_m
from my_token import TOKEN
# Enter your token here: TOKEN = "SOME VALUE"
m_m.bot = telebot.TeleBot(TOKEN)

db_vm.connect_database()

@m_m.bot.message_handler(commands=['start', 'help', 'hide', 'show', 'delete_me'])
def commands_listener(message):
    chat_id = message.chat.id
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

@m_m.bot.message_handler(func = lambda m: True)
def menu_buttons_listener(message):
    chat_id = message.chat.id
    # Main menu
    if message.text == m_m.Menu._learn:
        learning.start_learning(message)
    elif message.text == m_m.Menu._test:
        m_m.Menu.show_tests(chat_id)
    elif message.text == m_m.Menu._topic:
        m_m.bot.send_message(chat_id, "Topic changing is not implemented yet")
        # TODO: call command.change_topic(bot, chat_id)
    elif message.text == m_m.Menu._statistics:
        m_m.bot.send_message(chat_id, "Statistics is not implemented yet")
        # TODO: call command.show_statistics(bot, chat_id)

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
