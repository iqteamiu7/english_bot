import telebot

import database_viewmodel as db_vm
import main_model as m_m
from resourses import Emoji, Status

LEMOJI1 = '\U000027A1' #дальше
LEMOJI2 = '\U0001F6AB' # стоп
LEMOJI3 = '\U0001F3C1' #конец
LEMOJI4 = '\U0001F525' #огонь

BTN_NEXT = LEMOJI1 + " Next word"
BTN_START = LEMOJI4 + " GO!"
BTN_STOP = LEMOJI2 + " Stop"
HSW = 'Here are some new words for you'
NW = "All words in this topic are learned"
L_D = 'learning_data'
C_I = 'current_index'
T_L = LEMOJI3 + ' Thats all!'
S_Y = 'See you next time!'
MES_ER = Emoji.exclamation + 'please, send me only text messages'

#dic - словарь
#cur_i - current_index

def create_marcup(): #создание клавиш next word и stop
    u_m = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    u_m.add(telebot.types.KeyboardButton(text=BTN_NEXT))
    u_m.add(telebot.types.KeyboardButton(text=BTN_STOP))
    return u_m

def update_dictionary(cur_i, dic, chat_id): #обновление словаря, работа с бд
    dic.get(L_D)[cur_i].update({'il':True})
    dic.update({C_I: cur_i + 1})
    return dic

def start_learning(message): #начало обучения, приветствие
    db_vm.change_user_status(message.chat.id, Status.learning)
    u_m = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    u_m.add(telebot.types.KeyboardButton(text=BTN_START))
    dic = db_vm.get_unlearned_words(message.chat.id)

    if (0 < len(dic.get(L_D))):
        m_m.bot.send_message(message.chat.id, HSW, reply_markup=u_m)
        m_m.bot.register_next_step_handler(message, give_words, dic)
    else:
        m_m.bot.send_message(message.chat.id, NW)

def print_dic(dic):
    print("currect_index =", dic["current_index"])
    data = dic["learning_data"]
    print("learning_data")
    for i in data:
        print(i)
    print()

def give_words(message, dic): #обучение
    print_dic(dic)

    if type(message.text) != str:
        m_m.bot.send_message(message.chat.id, MES_ER)
        m_m.bot.register_next_step_handler(message, give_words, dic)
        return 'err'
    if message.text[0] == '/':
        m_m.bot.send_message(message.chat.id, Emoji.exclamation +
                "You can't enter commands during training or testing")
        m_m.bot.register_next_step_handler(message, give_words, dic)
        return

    u_m = create_marcup()
    cur_i = dic.pop(C_I)

    if message.text != BTN_STOP  and cur_i < len(dic.get(L_D)):
        e_w = dic.get(L_D)[cur_i].get('ew')
        r_w = dic.get(L_D)[cur_i].get('rw')
        m_m.bot.send_message(message.chat.id, e_w+' - '+r_w, reply_markup=u_m)
        dic = update_dictionary(cur_i, dic, message.chat.id)
        m_m.bot.register_next_step_handler(message, give_words, dic)
    else:
        db_vm.add_learned_words(message.chat.id, dic)
        db_vm.change_user_status(message.chat.id, Status.idle)
        u_m = m_m.Menu.get_main_markup()

        if cur_i >= len(dic.get(L_D)):
            m_m.bot.send_message(message.chat.id,T_L, reply_markup=u_m)
        else:
            m_m.bot.send_message(message.chat.id, S_Y, reply_markup=u_m)

if __name__ == "__main__":
    print("This is package file\n")
