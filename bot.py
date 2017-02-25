# -*- coding: utf-8 -*-
import telebot
import config
import random
import shelve

bot = telebot.TeleBot(config.token)

db_name = 'chat'
chat_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.god = None

class Chat:
    def __init__(self):
        self.user = None
        self.in_process = True

gods = {
    'иисус': 'Господу Богу твоему поклоняйся и Ему одному служи',
    'иисус христос': 'Люби Бога своего и всех людей',
    'аллах': 'Нет никакого божества, кроме Аллаха, и Мухаммад — посланник Аллаха!',
    'будда': 'Гармония приходит изнутри. Не ищите ее снаружи',
    'будда шакьямуни': 'Кувшин наполняется постепенно, капля за каплей',
    'яхва': 'Да прибудет с тобой сила',
    'бог яхва': 'Да прибудет с тобой сила',
    'конфуций': 'Да прибудет с тобой сила',
    'аматэрасу': 'Да прибудет с тобой сила',
    'заратустра': 'Да прибудет с тобой сила',
    'ахурамазда': 'Да прибудет с тобой сила',
    'ариман': 'Да прибудет с тобой сила',
    'путин': 'Я слежу за тобой, мой друг'
}


stickers = {
    'иисус': ['CAADAgADOAADGXMNCSqaRY-FOG6VAg'],
    'иисус христос': ['CAADAgADOAADGXMNCSqaRY-FOG6VAg'],
    'аллах': ['CAADBQADogAD_uTOAi1OxoF_OJCSAg'],
    'будда': ['CAADAwADfAADyzaRAAFVPCGbs0CdwAI'],
    'будда шакьямуни': ['CAADAwADfAADyzaRAAFVPCGbs0CdwAI'],
}



phrases = [
    'Да прибудет с тобой сила!',
    'Все твои молитвы будут услышаны',
    'Если твоей душе это будет угодно, ты обязательно это обретешь'
]

help_message = """\
Вы можете просто общаться с Богом на любые темы, задавать вопросы, что-то просить или воспользоваться следующими командами:

/start - Заново установить связь с Богом

/pray - Помолиться

/offertory - Сделать пожертвование
/help - Помощь
"""


@bot.message_handler(commands=['help'])
def send_help(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process == True:
        return

    msg = bot.send_message(chat_id, help_message)


@bot.message_handler(commands=['pray'])
def send_help(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process == True:
        return

    msg = bot.send_message(chat_id, """\
        pray
    """)


@bot.message_handler(commands=['offertory'])
def send_help(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process == True:
        return

    msg = bot.send_message(chat_id, """\
        offertory
    """)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process == True:
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
        if god_name in gods:
            if god_name in stickers:
                bot.send_sticker(chat_id, stickers[god_name][0])
            bot.send_message(chat_id, gods[god_name] + '\n\n' + help_message)


            user.god = god_name
            user.in_process = False

            db = shelve.open(db_name)
            db[str(chat_id)] = chat_dict[chat_id]
            db.close()

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

    if chat_id in chat_dict and chat_dict[chat_id].in_process == True:
        return

    db = shelve.open(db_name)
    chat = db.get(str(chat_id), default=None)
    db.close()

    if chat is None:
        bot.send_message(chat_id, random.choice(phrases))
    else:
        bot.send_message(chat_id, 'Оо, %s \n%s' %(chat.user.name, random.choice(phrases)))


if __name__ == '__main__':
    bot.polling(none_stop=True)

