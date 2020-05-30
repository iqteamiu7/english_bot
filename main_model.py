from telebot import types

from resourses import Emoji

bot = None

class Menu:
    _learn = Emoji.learn + " Start learning"
    _test = Emoji.test + " Start testing"
    _topic = Emoji.topic + " Change topic"
    _statistics = Emoji.statistics + " Show statistics"

    _active_test = Emoji.alien + " Active test"

    _go_to_main_menu = Emoji.back + " Go to main menu"

    @staticmethod
    def get_main_markup():
        markup = types.ReplyKeyboardMarkup(row_width = 1)

        learn_button = types.KeyboardButton(Menu._learn)
        test_button = types.KeyboardButton(Menu._test)
        topic_button = types.KeyboardButton(Menu._topic)
        statistics_button = types.KeyboardButton(Menu._statistics)

        markup.add(learn_button, test_button, topic_button, statistics_button)
        return markup
 
    @staticmethod
    def show_main(chat_id):
        markup = Menu.get_main_markup()
        bot.send_message(chat_id, "Main menu", reply_markup=markup)

    @staticmethod
    def get_tests_markup():
        markup = types.ReplyKeyboardMarkup(row_width = 1)

        active_test_button = types.KeyboardButton(Menu._active_test)
        main_menu_button = types.KeyboardButton(Menu._go_to_main_menu)

        markup.add(active_test_button, main_menu_button)
        return markup

    @staticmethod
    def show_tests(chat_id):
        markup = Menu.get_tests_markup()
        bot.send_message(chat_id, "Choose test", reply_markup=markup)

    @staticmethod
    def get_hide_markup():
        return types.ReplyKeyboardRemove(selective=False)

    @staticmethod
    def hide(chat_id):
        markup = Menu.get_hide_markup()
        bot.send_message(chat_id, "Menu is hidden", reply_markup=markup)

if __name__ == "__main__":
    print("This is package file\n")
