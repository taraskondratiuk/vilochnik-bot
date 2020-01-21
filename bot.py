import telebot
import os

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])


#pytelegrambotapi
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.infinity_polling()
