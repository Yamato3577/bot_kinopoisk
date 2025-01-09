from typing import Dict
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.smiles import smile_repeat, smile_check


def output_movie_names(data_movies: Dict, from_is: str = None) -> InlineKeyboardMarkup:
    """
    Формирует InlineKeyboard из списка  фильмов.
    Если вызывается из "поиска по параметрам", формирует дополнительную клавишу "Найти еще".
    :param data_movies: Dict
    найденные фильмы
    :param from_is: str = None
    от куда вызывается клавиатура
    :return: InlineKeyboardMarkup
    """

    markup = InlineKeyboardMarkup()
    for index, movie in enumerate(data_movies.get('docs')):
        name = movie.get('name')
        year = movie.get('year')
        if movie.get('views'):
            line = f'{smile_check} {name} ({year})'
        else:
            line = f'{name} ({year})'
        markup.add(InlineKeyboardButton(text=line, callback_data=str(index)))
    if from_is == 'search_param':
        markup.add(InlineKeyboardButton(text=f'{smile_repeat} Найти еще {smile_repeat}', callback_data='again'))
    return markup
