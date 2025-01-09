from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def genres_keyboard_one() -> InlineKeyboardMarkup:
    """
    Динамическая клавиатура для выбора жанра картины.
    :return: InlineKeyboardMarkup
    """

    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton(text='Боевик', callback_data='боевик'),
               InlineKeyboardButton(text='Триллер', callback_data='триллер'),
               InlineKeyboardButton(text='Комедия', callback_data='комедия'),
               InlineKeyboardButton(text='Ужасы', callback_data='ужасы'),
               InlineKeyboardButton(text='Фантастика', callback_data='фантастика'),
               InlineKeyboardButton(text='Фэнтези', callback_data='фэнтези'),
               InlineKeyboardButton(text='Вперед \U0001F449', callback_data='next_two'))
    return markup


def genres_keyboard_two() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton(text='Приключения', callback_data='приключения'),
               InlineKeyboardButton(text='История', callback_data='история'),
               InlineKeyboardButton(text='Вестерн', callback_data='вестерн'),
               InlineKeyboardButton(text='Драма', callback_data='драма'),
               InlineKeyboardButton(text='Мелодрама', callback_data='мелодрама'),
               InlineKeyboardButton(text='Детектив', callback_data='детектив'),
               InlineKeyboardButton(text='\U0001F448 Назад', callback_data='back_one'),
               InlineKeyboardButton(text='Вперед \U0001F449', callback_data='next_three'))
    return markup


def genres_keyboard_three() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton(text='Военные', callback_data='военный'),
               InlineKeyboardButton(text='Биография', callback_data='биография'),
               InlineKeyboardButton(text='Семейный', callback_data='семейный'),
               InlineKeyboardButton(text='Мюзикл', callback_data='мюзикл'),
               InlineKeyboardButton(text='Мультфильм', callback_data='мультфильм'),
               InlineKeyboardButton(text='Аниме', callback_data='аниме'),
               InlineKeyboardButton(text='\U0001F448 Назад', callback_data='back_two'))
    return markup
