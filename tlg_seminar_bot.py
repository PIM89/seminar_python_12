import telebot
import config
from telebot import types
import random
from datetime import datetime
import requests

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    stiker = open('stikers/smeh.tgs', 'rb')
    bot.send_sticker(message.chat.id, stiker)    
    user_full_name = message.from_user.full_name
    bot.send_message(message.chat.id, f'Привет, {user_full_name} ✌️\n'
    'Функции бота:\n'
    'Орел или решка (делать или не делать)\n'
    'Запрос курса биткоина\n'
    'Запрос номера телефона\n'
    'Как дела?\n'
    'Запуск функционала /button')
    # bot.send_message(message.chat.id, message)

@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Орел или решка")
    item2 = types.KeyboardButton("Запрос курса биткоина")
    item3 = types.KeyboardButton("Запрос номера телефона")
    item4 = types.KeyboardButton("Как дела?")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.chat.type == 'private':
        if message.text == 'Орел или решка':
            number = random.randint(0, 2)
            if number == 0:
                bot.send_message(message.chat.id, 'Орел! Сделай это!')
            elif number == 1:
                bot.send_message(message.chat.id, 'Решка! Не делай! 🥲')
        elif message.text == 'Запрос курса биткоина':
            bot.send_message(message.chat.id, get_data())
        elif message.text == 'Запрос номера телефона':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kn1 = types.KeyboardButton("Предоставить номер телефона", request_contact=True)
            kn2 = types.KeyboardButton("Назад")
            markup.add(kn1, kn2)
            bot.send_message(message.chat.id, 'Нажмите кнопку ниже', reply_markup=markup)
        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Орел или решка")
            item2 = types.KeyboardButton("Запрос курса биткоина")
            item3 = types.KeyboardButton("Запрос номера телефона")
            item4 = types.KeyboardButton("Как дела?")
            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
        elif message.text == 'Как дела?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Плохо", callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Выбери вариант :)', reply_markup=markup)

def get_data():
    req = requests.get('https://yobit.net/api/3/ticker/btc_usd')
    response = req.json()
    sell_price = response['btc_usd']['sell']
    return f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nСтоимость BTC: {sell_price}$"

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
               bot.send_message(call.message.chat.id, '✌️')
            elif call.data == 'bad':
               bot.send_message(call.message.chat.id, 'Сочувствую!')
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.message_id, text='Как дела?', reply_markup=None)
    except Exception as e:
        print(repr(e))

bot.infinity_polling()