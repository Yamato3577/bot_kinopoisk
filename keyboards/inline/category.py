from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def category_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора типа картины.
    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Фильмы', callback_data='movie'),
               InlineKeyboardButton(text='Сериалы', callback_data='tv-series'))
    return markup
