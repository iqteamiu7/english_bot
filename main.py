import telebot

import database_viewmodel as db_vm
import command
import learning
import testing
from resourses import Emoji
from menu import Menu

from my_token import TOKEN
# Enter your token here: TOKEN = "SOME VALUE"
bot = telebot.TeleBot(TOKEN)

db_vm.connect_database()

@bot.message_handler(commands=['start', 'help', 'hide', 'show', 'delete_me'])
def commands_listener(message):
    chat_id = message.chat.id
    if message.text.find("/start") == 0:
        command.on_start(bot, message)
    elif message.text.find("/help") == 0:
        command.on_help(bot, chat_id)
    elif message.text.find("/hide") == 0:
        Menu.hide(bot, chat_id)
    elif message.text.find("/show") == 0:
        Menu.show_main(bot, chat_id)
    elif message.text.find("/delete_me") == 0:
        command.on_delete_me(bot, chat_id)

@bot.message_handler(func = lambda m: True)
def menu_buttons_listener(message):
    chat_id = message.chat.id
    # Main menu
    if message.text == Menu._learn:
        bot.send_message(chat_id, "Learning is not implemented yet")
        # TODO: call leaning.start_learning(bot, chat_id)
    elif message.text == Menu._test:
        Menu.show_tests(bot, chat_id)
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
        Menu.show_main(bot, chat_id)

    else:
        bot.send_message(chat_id, "Hmmmm... I don\'t understand")

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()
