import os

import redis
import telebot

from src.parser import matches_page_parser as mpp

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
db = redis.Redis(host=os.environ['DB_HOST'], port=int(os.environ['DB_PORT']))


@bot.message_handler(content_types=['text'], regexp='matches')
def get_todays_matches_info(message):
    db.append(message.text, 'cumshot')

    matches = mpp.get_matches_info()
    if matches:
        for m in matches:
            bot.send_message(message.chat.id, m, parse_mode='markdown')
    else:
        bot.send_message(message.chat.id, 'No matches for today!')


if __name__ == '__main__':
    bot.infinity_polling()
