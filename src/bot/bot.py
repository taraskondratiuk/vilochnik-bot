import os

import redis
import telebot

from src.parser import matches_page_parser as mpp

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
# db = redis.Redis(host=os.environ['DB_HOST'], port=int(os.environ['DB_PORT']))


@bot.message_handler(content_types=['text'], regexp='matches')
def get_todays_matches_info(message):
    # db.append(message.text, 'cumshot')
    for match in mpp.get_matches_info():
        bot.send_message(message.chat.id, match, parse_mode="markdown")


if __name__ == '__main__':
    bot.infinity_polling()
