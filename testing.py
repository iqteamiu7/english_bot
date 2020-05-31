import random

import telebot

import database_viewmodel as db_vm
import main_model as m_m
from resourses import Emoji, Status

EMOJI1 = '\U00002705' #галочка
EMOJI2 = '\U0000274C' #крестик
EMOJI3 = '\U0001F3C1' #конец
L_D = 'testing_data'
C_I = 'current_index'
Y_R = EMOJI1 + ' You are right'
Y_W = EMOJI2 + ' You are wrong'
R_A = 'The right answer is: '
WTM = 'What is the meaning of: '
WTE = 'What is the english for: '
G_J = EMOJI3 + ' Thats all, good job!'
C_L = 'Come again later'
NW = "You haven't learned a single word in this topic"
MES_ER = Emoji.exclamation + 'please, send me only text messages' 

#dic - словарь
#cur_i - current_index
#lang - language
#t_w - testing_word
#ans - answer

def update_dictionary(cur_i , dic, iactc, chat_id): #обновление словаря
    dic.get(L_D)[cur_i].update({'iactc':iactc})
    dic.update({C_I : cur_i + 1})
    return dic

def find_answer(dic, cur_i, ans, t_w): #проверка ответа
    e_w = dic.get(L_D)[cur_i].get('ew')
    r_w = dic.get(L_D)[cur_i].get('rw')

    if e_w == ans and  r_w == t_w and ans != t_w:
        return 'yes'
    if r_w == ans and e_w == t_w and ans != t_w:
        return 'yes'
    return 'no'

def show_answer(message, dic, cur_i, lang): #демонстрация ответа
    if lang == 0:
        ans = dic.get(L_D)[cur_i].get('rw')
    else:
        ans = dic.get(L_D)[cur_i].get('ew')
    m_m.bot.send_message(message.chat.id, R_A + ans)

def start_testing(message): #начало тестирования
    chat_id = message.chat.id
    db_vm.change_user_status(message.chat.id, Status.testing)

    dic = db_vm.get_learned_words(message.chat.id)
    print_dic(dic)
    cur_i = dic.get(C_I)

    if (cur_i < len(dic.get(L_D))):
        markup = m_m.Menu.get_hide_markup()
        m_m.bot.send_message(
            chat_id,
            "You can stop testing by entering\n/stop_testing",
            reply_markup = markup
            )
        t_w = dic.get(L_D)[cur_i].get('ew')
        m_m.bot.send_message(chat_id, WTM+'"'+t_w+'"?')
        m_m.bot.register_next_step_handler(message, testing, dic, 0)
    else:
        m_m.bot.send_message(chat_id, NW)
        db_vm.change_user_status(message.chat.id, Status.idle)

def print_dic(dic):
    print("currect_index =", dic["current_index"])
    data = dic["testing_data"]
    print("learning_data")
    for i in data:
        print(i)
    print()

def testing(message, dic, lang): #тестирование
    print_dic(dic)

    if type(message.text) == str:
        ans = message.text.lower()
    else:
        m_m.bot.send_message(message.chat.id, MES_ER)
        m_m.bot.register_next_step_handler(message, testing, dic, lang)
        return 'err'

    if message.text[0] == '/' and message.text.find("/stop_testing") != 0:
        m_m.bot.send_message(message.chat.id, Emoji.exclamation +
                "You can use only one command during testing:\n/stop_testing")
        m_m.bot.register_next_step_handler(message, testing, dic, lang)
        return

    cur_i = dic.get(C_I)
    ans = message.text.lower()

    if cur_i < len(dic.get(L_D)) and ans != '/stop_testing':
        e_w = dic.get(L_D)[cur_i].get('ew')
        r_w = dic.get(L_D)[cur_i].get('rw')

        if  ((lang == 0 and find_answer(dic, cur_i, ans, e_w) == 'yes')\
        or (lang == 1 and  find_answer(dic, cur_i, ans, r_w) == 'yes')):
            m_m.bot.send_message(message.chat.id, Y_R)
            iactc = True
        else:
            m_m.bot.send_message(message.chat.id, Y_W)
            show_answer(message, dic, cur_i, lang)
            iactc = False
        dic = update_dictionary(cur_i, dic, iactc, message.chat.id)
        cur_i = dic.get(C_I)

        if cur_i < len(dic.get(L_D)) and ans != '/stop_testing':
            random.seed()
            lang = random.randint(0,1)

            if lang == 0:
                t_w = dic.get(L_D)[cur_i].get('ew')
                m_m.bot.send_message(message.chat.id, WTM+'"'+t_w+'"?')
            else:
               t_w = dic.get(L_D)[cur_i].get('rw')
               m_m.bot.send_message(message.chat.id, WTE+'"'+t_w+'"?')
            m_m.bot.register_next_step_handler(message, testing, dic, lang)
        else:
            db_vm.update_learned_words(message.chat.id, dic)
            db_vm.change_user_status(message.chat.id, Status.idle)
            markup = m_m.Menu.get_main_markup()
            m_m.bot.send_message(message.chat.id, G_J, reply_markup = markup)
    if ans == '/stop_testing':
        db_vm.update_learned_words(message.chat.id, dic)
        db_vm.change_user_status(message.chat.id, Status.idle)
        markup = m_m.Menu.get_main_markup()
        m_m.bot.send_message(message.chat.id, C_L, reply_markup = markup)

if __name__ == "__main__":
    print("This is package file\n")
