# -*- coding: utf-8 -*-

import telebot
from telebot import types
import random
from helper import *
import static as st

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['help'])
def send_help(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process is True:
        return

    msg = bot.send_message(chat_id, st.help_message)

@bot.message_handler(commands=['prayerbook'])
def send_prayerbook(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process is True:
        return

    chat = Chat.get_from_db(chat_id)
    if chat is None:
        msg = bot.send_message(chat_id, st.plz_registrate)
    else:
        markup = types.ReplyKeyboardMarkup()
        for prayer_name in st.gods[chat.user.god].prayers.keys():
            markup.row(prayer_name)
        markup.row(st.cancel)

        msg = bot.send_message(chat_id, """\
            О чем Ты хочешь помолиться?
        """, reply_markup=markup)
        bot.register_next_step_handler(msg, process_prayer_step)
        chat_dict[chat_id] = chat


def process_prayer_step(message):
    chat_id = message.chat.id

    prayer_name = message.text.encode('utf-8')
    if prayer_name == st.cancel:
        keyboard_hider = types.ReplyKeyboardRemove()
        bot.send_message(chat_id, random.choice(st.phrases), reply_markup=keyboard_hider)
        chat_dict.pop(chat_id)
    else:
        prayers = st.gods[chat_dict[chat_id].user.god].prayers
        if prayer_name in prayers:
            msg = bot.send_voice(chat_id, prayers[prayer_name].audio_file_id)
        else:
            msg = bot.send_message(chat_id, 'Я не знаю такой молитвы')
        bot.register_next_step_handler(msg, process_prayer_step)


@bot.message_handler(commands=['pray'])
def send_pray(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process is True:
        return

    chat = Chat.get_from_db(chat_id)
    if chat is None:
        msg = bot.send_message(chat_id, st.plz_registrate)
    else:
        msg = bot.send_message(chat_id, """\
            Отправь контакт близкого человека, к которому обращена Твоя молитва (и ему придет оповещение) или назови его имя
        """)
        bot.register_next_step_handler(msg, process_pray_for)
        chat_dict[chat_id] = chat


def process_pray_for(message):
    chat_id = message.chat.id

    chat_dict[chat_id].temp_message = message

    msg = bot.send_message(chat_id, 'Запишите для него молитву в текстовой или голосовой форме')
    bot.register_next_step_handler(msg, process_pray_text)


def process_pray_text(message):
    chat = message.chat
    chat_id = chat.id

    prev_message = chat_dict[chat_id].temp_message
    if prev_message.contact is not None:
        save_contact(prev_message.contact)
        #send notification to him
        name = prev_message.contact.first_name.encode("UTF-8") + ' ' + prev_message.contact.last_name.encode("UTF-8")
    else:
        name = prev_message.text.encode("UTF-8")
    bot.send_message(chat_id, random.choice([st.prayer_listened % name, st.prayer_not_listened]))

    chat_dict.pop(chat_id)


@bot.message_handler(commands=['offertory'])
def send_offertory(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process is True:
        return

    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Сделать пожертвование", url="http://yasobe.ru/na/vnezemnoeblago")
    keyboard.add(url_button)    

    msg = bot.send_message(chat_id, st.offertory_message, reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process is True:
        return

    msg = bot.send_message(chat_id, """\
    Приветствую тебя! Назови свое имя, Сын мой
    """)
    bot.register_next_step_handler(msg, process_name_step)
    chat = Chat()
    chat_dict[chat_id] = chat


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text.encode('utf-8')
        user = User(name)
        chat_dict[chat_id].user = user
        msg = bot.send_message(chat_id, user.name + ', кто является твоим Богом?')
        bot.register_next_step_handler(msg, process_god_name)
    except Exception as e:
        bot.send_message(chat_id, 'oooops')


def process_god_name(message):
    try:
        chat_id = message.chat.id
        god_name = message.text.lower().encode('utf-8')

        if chat_id in chat_dict:
            user = chat_dict[chat_id].user
        if god_name in st.gods:
            relig = st.gods[god_name]
            if relig.stickers:
                bot.send_sticker(chat_id, random.choice(relig.stickers))
            bot.send_message(chat_id, random.choice(relig.hello_phrases) + '\n\n' + st.help_message)

            user.god = god_name

            Chat.save_to_db(chat_id)

            chat_dict.pop(chat_id, None)
        else:
            msg = bot.send_message(chat_id, 'Я не знаю такого Бога, попробуй еще раз...')
            bot.register_next_step_handler(msg, process_god_name)
    except Exception as e:
        bot.send_message(chat_id, 'oooops')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def repeat_all_messages(message):
    chat_id = message.chat.id

    print str(chat_id) + ': ' + message.text

    if chat_id in chat_dict and chat_dict[chat_id].in_process is True:
        return

    chat = Chat.get_from_db(chat_id)

    if chat is None:
        bot.send_message(chat_id, random.choice(st.phrases))
    else:
        bot.send_message(chat_id, 'Оо, %s \n%s' % (chat.user.name, random.choice(st.phrases)))


