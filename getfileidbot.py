# -*- coding: utf-8 -*-
import telebot
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['sticker'])
def getfileid(message):
    file_id = message.sticker.file_id
    bot.send_message(message.chat.id, file_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)