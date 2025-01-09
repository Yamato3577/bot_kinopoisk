from loguru import logger

from typing import Dict, Union
from telebot.types import Message, CallbackQuery

from keyboards.inline.choosing_action import choosing_action
from loader import bot


def print_info_movie(message: Union[Message, CallbackQuery], movie: Dict,
                     index_movie: int = 0, from_is: str = None) -> Dict:
    """
    Вывод информации выбранного фильма пользователю и формирование словаря для записи в БД.
    :param message: Union[Message, CallbackQuery]
    :param movie: Dict
    Словарь с найденными фильмами(до 5)
    :param index_movie: int = 0
    Индекс фильма в списке
    :param from_is: str = None
    От куда вызывается вывод информации о фильме, на основании формируется клавиатура навигации.
    :return: Dict
    Словарь для записи фильма в БД
    """

    translation_types = {'movie': 'Фильм', 'tv-series': 'Сериал', 'cartoon': 'Мультфильм',
                         'anime': 'Аниме', 'animated-series': 'Мультсериал'}

    if type(message).__name__ == 'Message':
        chat_id = message.chat.id
    else:
        chat_id = message.message.chat.id

    try:
        film = movie.get('docs')[index_movie]
        type_movie = film.get('type', {'нет информации'})
        countries = ', '.join([country['name'] for country in film.get('countries')])
        poster = film.get('poster', {}).get('previewUrl')
        trailer = film.get('videos', {}).get('trailers', {})
        if trailer:
            trailer = trailer[0].get('url')
        else:
            trailer = 'нет трейлера'
        name = film.get('name', {'нет информации'})
        id_movie = film.get('id')
        year = film.get('year', {'нет информации'})
        rating_kp = float(round(film.get('rating', {}).get('kp'), 1))
        description = film.get('description', {'нет описания'})
        genres = ', '.join([genre['name'] for genre in film.get('genres')])

        info_movie = {'id': id_movie, 'name': name, 'type': type_movie,  'countries': countries,
                      'description': description, 'year': year, 'poster': poster, 'genres': genres, 'rating': rating_kp,
                      'trailer': trailer}
        text = (f'<b>Название:</b> {name}\n'
                f'<b>Тип:</b> {translation_types[type_movie]}\n'
                f'<b>Страна:</b> {countries}\n'
                f'<b>Год:</b> {year}\n'
                f'<b>Жанр:</b> {genres}\n'
                f'<b>Рейтинг KP:</b> {rating_kp}\n'
                f'<b>Трейлер:</b> {trailer}\n'
                f'<b>Описание фильма:</b> {description}'
                )
        if len(text) > 1024:
            text = text[:1021] + '...'

        bot.send_photo(chat_id,
                       poster,
                       caption=text,
                       parse_mode='HTML',
                       reply_markup=choosing_action(message.from_user.id, id_movie, from_is)
                       )
        return info_movie

    except Exception as error:
        bot.send_message(chat_id, 'Недостаточно информации, откройте другой фильм')
        logger.error('Пользователь {}, ошибка {}', message.from_user.username, error)
