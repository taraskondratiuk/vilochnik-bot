import telebot
import os
import redis

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
db = redis.Redis(host=os.environ['DB_HOST'], port=int(os.environ['DB_PORT']))


@bot.message_handler(content_types=["text"], regexp='matches')
def get_todays_matches_info(message):
    db.append(message.text, 'cumshot')
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.infinity_polling()
