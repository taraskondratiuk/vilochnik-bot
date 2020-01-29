import os
import threading
import time

import redis
import schedule
import telebot

from ..bot.keyboard import generate_keyboard
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
    keyboard = generate_keyboard('matches', 'unsubscribe')
    bot.send_message(message.chat.id, 'You subscribed to notifications!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'], regexp='unsubscribe')
def unsubscribe_from_notifications(message):
    db.srem('ids', message.chat.id)
    keyboard = generate_keyboard('matches', 'subscribe')
    bot.send_message(message.chat.id, 'You unsubscribed from notifications!', reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = generate_keyboard('matches', 'subscribe')
    bot.send_message(message.chat.id,
                     'Get today\'s matches info or subscribe to daily notifications',
                     reply_markup=keyboard)


def send_matches_info_to_subscribers():
    subs_chat_ids = db.smembers('ids')
    matches = get_matches_info()
    for i in subs_chat_ids:
        __send_matches_info(int(i), matches)


def __send_matches_info(chat_id, matches):
    if matches:
        for m in matches:
            bot.send_message(chat_id, m, parse_mode='markdown', disable_web_page_preview=True)
    else:
        bot.send_message(chat_id, 'No matches for today!')


def run_polling():
    bot.infinity_polling()


def run_notifications_scheduler():
    schedule.every().day.at(notification_time).do(send_matches_info_to_subscribers)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == '__main__':
    t1 = threading.Thread(target=run_polling)
    t2 = threading.Thread(target=run_notifications_scheduler)
    t1.start()
    t2.start()
