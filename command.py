from resourses import Emoji

def on_start(bot, chat_id):
    bot.send_message(chat_id, "Hello " + Emoji.hello)
    bot.send_message(chat_id, "I will help you learn words in English " +
            Emoji.tea_cap)
    bot.send_message(chat_id, "We will communicate using the buttons" +
            Emoji.finger_down)
    # TODO: add work with database

def on_help(bot, chat_id):
    # TODO: come up with a useful message
    bot.send_message(chat_id, "Unhelpful message\n¯\_(ツ)_/¯")

if __name__ == "__main__":
    print("This is package file")
