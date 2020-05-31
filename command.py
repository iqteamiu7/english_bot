import main_model as m_m
from resourses import Emoji
import database_viewmodel as db_vm

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

if __name__ == "__main__":
    print("This is package file\n")
