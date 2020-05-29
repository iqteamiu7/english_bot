import telebot
from telebot import types

import database_viewmodel as db_vm
import command
import learning
import testing
from resourses import Emoji

from my_token import TOKEN
# Enter your token here: TOKEN = "SOME VALUE"
bot = telebot.TeleBot(TOKEN)

db_vm.connect_database()

class Menu:
    _learn = Emoji.learn + " Start learning"
    _test = Emoji.test + " Start testing"
    _topic = Emoji.topic + " Change topic"
    _statistics = Emoji.statistics + " Show statistics"

    _active_test = Emoji.alien + " Active test"

    _go_to_main_menu = Emoji.back + " Go to main menu"

    @staticmethod
    def show_main(chat_id):
        markup = types.ReplyKeyboardMarkup(row_width = 1)

        learn_button = types.KeyboardButton(Menu._learn)
        test_button = types.KeyboardButton(Menu._test)
        topic_button = types.KeyboardButton(Menu._topic)
        statistics_button = types.KeyboardButton(Menu._statistics)

        markup.add(learn_button, test_button, topic_button, statistics_button)
        bot.send_message(chat_id, "Main menu", reply_markup=markup)

    @staticmethod
    def show_tests(chat_id):
        markup = types.ReplyKeyboardMarkup(row_width = 1)

        active_test_button = types.KeyboardButton(Menu._active_test)
        main_menu_button = types.KeyboardButton(Menu._go_to_main_menu)

        markup.add(active_test_button, main_menu_button)
        bot.send_message(chat_id, "Choose test", reply_markup=markup)

    @staticmethod
    def hide(chat_id):
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(chat_id, "Menu is hidden", reply_markup=markup)

@bot.message_handler(commands=['start', 'help', 'hide', 'show'])
def commands_listener(message):
    chat_id = message.chat.id
    if message.text.find("/start") == 0:
        command.on_start(bot, chat_id)
    elif message.text.find("/help") == 0:
        command.on_help(bot, chat_id)
    elif message.text.find("/hide") == 0:
        Menu.hide(chat_id)
    elif message.text.find("/show") == 0:
        Menu.show_main(chat_id)

@bot.message_handler(func = lambda m: True)
def menu_buttons_listener(message):
    chat_id = message.chat.id
    # Main menu
    if message.text == Menu._learn:
        bot.send_message(chat_id, "Learning is not implemented yet")
        # TODO: call leaning.start_learning(bot, chat_id)
    elif message.text == Menu._test:
        Menu.show_tests(chat_id)
    elif message.text == Menu._topic:
        bot.send_message(chat_id, "Topic changing is not implemented yet")
        # TODO: call command.change_topic(bot, chat_id)
    elif message.text == Menu._statistics:
        bot.send_message(chat_id, "Statistics is not implemented yet")
        # TODO: call command.show_statistics(bot, chat_id)

    # Test menu
    elif message.text == Menu._active_test:
        bot.send_message(chat_id, "Active test is not implemented yet")
        # TODO: call leaning.start_testing(bot, chat_id)
    elif message.text == Menu._go_to_main_menu:
        Menu.show_main(chat_id)

    else:
        bot.send_message(chat_id, "Hmmmm... I don\'t understand")

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()
