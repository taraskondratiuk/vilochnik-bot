from telebot import types


def generate_keyboard(first_button, second_button):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.add(first_button, second_button)
    return markup
