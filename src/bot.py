import os

import redis
import telebot
from keyboard import generate_keyboard
from matches_page_parser import get_matches_info

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
db = redis.Redis(host=os.environ['DB_HOST'], port=int(os.environ['DB_PORT']))
notification_time = os.environ['NOTIFICATION_TIME']
hours_offset = float(os.environ['HOURS_OFFSET'])


@bot.message_handler(content_types=['text'], regexp='matches')
def get_todays_matches_info(message):
    matches = get_matches_info(hours_offset)
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


def __send_matches_info(chat_id, matches):
    if matches:
        for m in matches:
            bot.send_message(chat_id, m, parse_mode='markdown', disable_web_page_preview=True)
    else:
        bot.send_message(chat_id, 'No matches for today!')


if __name__ == '__main__':
    bot.infinity_polling()
