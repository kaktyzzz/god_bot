# -*- coding: utf-8 -*-

import shelve
import config


chat_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.god = None


class ShelveDB:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.db = shelve.open(self.db_name)
        return self.db

    def __exit__(self, *args):
        self.db.close()


class Chat:
    def __init__(self, user=None):
        self.user = user
        self.in_process = True
        self.temp_message = ''

    @staticmethod
    def get_from_db(chat_id):
        with ShelveDB(config.DB_NAME) as db:
            chat = Chat(db.get(str(chat_id), default=None))

        return chat

    @staticmethod
    def save_to_db(chat_id):
        with ShelveDB(config.DB_NAME) as db:
            db[str(chat_id)] = chat_dict[chat_id].user


class Prayer:
    def __init__(self, audio_file_id=None, text='', for_human=False):
        self.audio_file_id = audio_file_id
        self.text = text
        self.for_human = for_human



class Religious:
    def __init__(self, name, hello_phrase=['Да прибудет с тобой сила'], stickers=[], prayers={}):
        self.name = name
        self.hello_phrases = hello_phrase
        self.stickers = stickers
        self.prayers = prayers
