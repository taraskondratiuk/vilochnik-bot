import os
import threading
import time

import redis
import schedule
import telebot

from ..parser.matches_page_parser import get_matches_info

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
db = redis.Redis(host=os.environ['DB_HOST'], port=int(os.environ['DB_PORT']))
notification_time = os.environ['NOTIFICATION_TIME']


@bot.message_handler(content_types=['text'], regexp='matches')
def get_todays_matches_info(message):
    matches = get_matches_info()
    __send_matches_info(message.chat.id, matches)


@bot.message_handler(content_types=['text'], regexp='subscribe')
def subscribe_for_notifications(message):
    db.sadd('ids', message.chat.id)


@bot.message_handler(content_types=['text'], regexp='unsubscribe')
def unsubscribe_from_notifications(message):
    db.srem('ids', message.chat.id)


def send_matches_info_to_subscribers():
    subs_chat_ids = db.smembers('ids')
    matches = get_matches_info()
    for i in subs_chat_ids:
        __send_matches_info(int(i), matches)


def __send_matches_info(chat_id, matches):
    if matches:
        for m in matches:
            bot.send_message(chat_id, m, parse_mode='markdown')
    else:
        bot.send_message(chat_id, 'No matches for today!')


def run_bot():
    bot.infinity_polling()


def run_scheduler():
    schedule.every().day.at(notification_time).do(send_matches_info_to_subscribers)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == '__main__':
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=run_scheduler)
    t1.start()
    t2.start()
