from telebot import types

from resourses import Emoji

class Menu:
    _learn = Emoji.learn + " Start learning"
    _test = Emoji.test + " Start testing"
    _topic = Emoji.topic + " Change topic"
    _statistics = Emoji.statistics + " Show statistics"

    _active_test = Emoji.alien + " Active test"

    _go_to_main_menu = Emoji.back + " Go to main menu"

    @staticmethod
    def show_main(bot, chat_id):
        markup = types.ReplyKeyboardMarkup(row_width = 1)

        learn_button = types.KeyboardButton(Menu._learn)
        test_button = types.KeyboardButton(Menu._test)
        topic_button = types.KeyboardButton(Menu._topic)
        statistics_button = types.KeyboardButton(Menu._statistics)

        markup.add(learn_button, test_button, topic_button, statistics_button)
        bot.send_message(chat_id, "Main menu", reply_markup=markup)

    @staticmethod
    def show_tests(bot, chat_id):
        markup = types.ReplyKeyboardMarkup(row_width = 1)

        active_test_button = types.KeyboardButton(Menu._active_test)
        main_menu_button = types.KeyboardButton(Menu._go_to_main_menu)

        markup.add(active_test_button, main_menu_button)
        bot.send_message(chat_id, "Choose test", reply_markup=markup)

    @staticmethod
    def hide(bot, chat_id):
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(chat_id, "Menu is hidden", reply_markup=markup)

if __name__ == "__main__":
    print("This is package file\n")
