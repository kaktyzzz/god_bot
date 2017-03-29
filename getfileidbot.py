# -*- coding: utf-8 -*-
import telebot
import config
import os
import time
import logging

bot = telebot.TeleBot(config.TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

MUSIC_DIR = 'music'
LOADED_DIR = os.path.join(MUSIC_DIR, 'loaded')
FILE_IDS_FILE = os.path.join(LOADED_DIR, 'file_ids.txt')

@bot.message_handler(content_types=['sticker'])
def getfileid(message):
    file_id = message.sticker.file_id
    bot.send_message(message.chat.id, file_id)

@bot.message_handler(content_types=['text'])
def getfileid(message):
    with open(FILE_IDS_FILE, 'a') as f:
        for file in os.listdir(MUSIC_DIR):
            if file.split('.')[-1] == 'ogg':
                ret_msg = bot.send_voice(message.chat.id, open(os.path.join(MUSIC_DIR, file), 'rb'))
                f.write(file + ' ' + ret_msg.voice.file_id + '\n')
                os.rename(os.path.join(MUSIC_DIR, file), os.path.join(LOADED_DIR, file))



@bot.message_handler(content_types=['voice'])
def getfileid(message):

    file_info = bot.get_file(message.voice.file_id)

    downloaded_file = bot.download_file(file_info.file_path)

    with open('new_file.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)


if __name__ == '__main__':
    bot.polling(none_stop=True)