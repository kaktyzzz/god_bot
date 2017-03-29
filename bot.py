# -*- coding: utf-8 -*-
import telebot
from telebot import types
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

    @staticmethod
    def get_from_db(chat_id):
        db = shelve.open(db_name)
        chat = db.get(str(chat_id), default=None)
        db.close()

        return chat

    @staticmethod
    def save_to_db(chat_id):
        db = shelve.open(db_name)
        db[str(chat_id)] = chat_dict[chat_id]
        db.close()


class Religious:
    def __init__(self, name, hello_phrase=['Да прибудет с тобой сила'], stickers=[], prayers={}):
        self.name = name
        self.hello_phrases = hello_phrase
        self.stickers = stickers
        self.prayers = prayers


hrist = Religious(
                'Христианство',
                ['Господу Богу твоему поклоняйся и Ему одному служи', 'Люби Бога своего и всех людей'],
                ['CAADAgADOAADGXMNCSqaRY-FOG6VAg'],
                {
                    'Отче наш':'AwADAgADVwADW5rZSvekof0PkgZBAg',
                    'Песнь Богородицы': 'AwADAgADVQADW5rZSjicBmlpyILRAg',
                    'Символ веры': 'AwADAgADWAADW5rZSj2pan7ZxRsmAg',
                    'Молитва кресту': 'AwADAgADVgADW5rZSryvl4hANtGxAg',
                })

buddizm = Religious(
                'Буддизм',
                ['Гармония приходит изнутри. Не ищите ее снаружи'],
                ['CAADAwADfAADyzaRAAFVPCGbs0CdwAI'])

gods = {
    'иисус': hrist,
    'иисус христос': hrist,
    'аллах': Religious(
                'Ислам',
                ['Нет никакого божества, кроме Аллаха, и Мухаммад — посланник Аллаха!'],
                 ['CAADBQADogAD_uTOAi1OxoF_OJCSAg']),
    'будда': buddizm,
    'будда шакьямуни': buddizm,
    'яхва': Religious(''),
    'бог яхва': Religious(''),
    'конфуций': Religious(''),
    'аматэрасу': Religious(''),
    'заратустра': Religious(''),
    'ахурамазда': Religious(''),
    'ариман': Religious(''),
    'путин': Religious(
                'Путин',
                ['Я слежу за тобой, мой друг'])
}

phrases = [
    'Да прибудет с тобой сила!',
    'Все твои молитвы будут услышаны',
    'Если твоей душе это будет угодно, ты обязательно это обретешь'
]

plz_registrate = 'Пожалуйста, установите контакт с Богом'
cancel = 'Отмена'

help_message = """\
Вы можете просто общаться с Богом на любые темы, задавать вопросы, что-то просить или воспользоваться следующими командами:

/start - Заново установить контакт с Богом

/prayerbook - Молитвенник

/pray - Помолиться за раба Божьего

/offertory - Сделать пожертвование
/help - Помощь
"""


@bot.message_handler(commands=['help'])
def send_help(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process is True:
        return

    msg = bot.send_message(chat_id, help_message)

@bot.message_handler(commands=['prayerbook'])
def send_prayerbook(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process is True:
        return

    chat = Chat.get_from_db(chat_id)
    if chat is None:
        msg = bot.send_message(chat_id, plz_registrate)
    else:
        markup = types.ReplyKeyboardMarkup()
        for prayer_name in gods[chat.user.god].prayers.keys():
            markup.row(prayer_name)
        markup.row(cancel)

        msg = bot.send_message(chat_id, """\
            Выберите молитву
        """, reply_markup=markup)
        bot.register_next_step_handler(msg, process_prayer_step)
        chat.in_process = True
        chat_dict[chat_id] = chat


def process_prayer_step(message):
    chat_id = message.chat.id

    prayer_name = message.text.encode('utf-8')
    if prayer_name == cancel:
        keyboard_hider = types.ReplyKeyboardRemove()
        bot.send_message(chat_id, random.choice(phrases), reply_markup=keyboard_hider)
        chat_dict.pop(chat_id)
    else:
        prayers = gods[chat_dict[chat_id].user.god].prayers
        if prayer_name in prayers:
            msg = bot.send_voice(chat_id, prayers[prayer_name])
        else:
            msg = bot.send_message(chat_id, 'Я не знаю такой молитвы')
        bot.register_next_step_handler(msg, process_prayer_step)





@bot.message_handler(commands=['pray'])
def send_pray(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process is True:
        return

    msg = bot.send_message(chat_id, """\
        pray
    """)


@bot.message_handler(commands=['offertory'])
def send_offertory(message):
    chat_id = message.chat.id

    if chat_id in chat_dict and chat_dict[chat_id].in_process is True:
        return

    msg = bot.send_message(chat_id, """\
        offertory
    """)


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
        if god_name in gods:
            relig = gods[god_name]
            if relig.stickers:
                bot.send_sticker(chat_id, random.choice(relig.stickers))
            bot.send_message(chat_id, random.choice(relig.hello_phrases) + '\n\n' + help_message)

            user.god = god_name
            user.in_process = False

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
        bot.send_message(chat_id, random.choice(phrases))
    else:
        bot.send_message(chat_id, 'Оо, %s \n%s' % (chat.user.name, random.choice(phrases)))


