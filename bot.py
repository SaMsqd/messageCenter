import telebot
from random import randint
import schedule


bot = telebot.TeleBot('6954703843:AAEecbqfqpbOA4-BsQi0E3I569Uus31Eu1A')


users_id = [643793566]
messege_id = {}


def send_password():
    global messege_id
    global password
    password = randint(100000, 999999)                  #рандомим пароль
    for elem in users_id:                                 #удаляем предыдущий и отправляем новый пароли каждому из юзеров
        bot.delete_message(elem,messege_id[elem])
        messege_id[elem] = bot.send_message(elem,f'<b>Пароль: {password}</b>', parse_mode='html').id


if __name__ == '__main__':
    for elem in users_id:
        messege_id[elem] = bot.send_message(elem,f'<b>Начнем работу</b>', parse_mode='html').id        #выводим первое сообщение так как send_password должна удалить предыдущее сообщение
    send_password()
    schedule.every().day.at('06:00').do(send_password)
    while True:
        schedule.run_pending()
