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
    def __init__(self):
        self.user = None
        self.in_process = True

    @staticmethod
    def get_from_db(chat_id):
        with ShelveDB(config.DB_NAME) as db:
            chat = db.get(str(chat_id), default=None)

        return chat

    @staticmethod
    def save_to_db(chat_id):
        with ShelveDB(config.DB_NAME) as db:
            db[str(chat_id)] = chat_dict[chat_id]


class Religious:
    def __init__(self, name, hello_phrase=['Да прибудет с тобой сила'], stickers=[], prayers={}):
        self.name = name
        self.hello_phrases = hello_phrase
        self.stickers = stickers
        self.prayers = prayers
