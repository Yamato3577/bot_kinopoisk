from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def search() -> InlineKeyboardMarkup:
    """
    Клавиатура для старта поиска по параметрам.
    :return: InlineKeyboardMarkup
    """

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Начать поиск', callback_data='search'))
    return markup
