from telebot.types import CallbackQuery

from handlers.custom_handlers.search_movie_param import print_movies
from keyboards.inline.movies import output_movie_names
from loader import bot
from database.CRUD import add_favourites, delete_favorite, checking_number_movies
from handlers.custom_handlers.favourites import print_favourites
from handlers.custom_handlers.info_movie import print_info_movie
from handlers.custom_handlers.random_movie import random_movie
from requests_api.kinopoisk import get_movie


@bot.callback_query_handler(func=lambda call: call.data in ['0', '1', '2', '3', '4'])
def print_info_choice_movie(call: CallbackQuery) -> None:
    """Обрабатывает нажатие клавиш из списка фильмов
     и открывает информацию + оставляет галочку на просмотренном фильме"""
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['info_movie'] = print_info_movie(call, data['result_search'], int(call.data), data['from_is'])
        data.get('result_search').get('docs')[int(call.data)]['views'] = True


@bot.callback_query_handler(func=lambda call: call.data in ['back_movies', 'back_favourites', 'add_favorites',
                                                            'del_movie_db', 'random', 'again'])
def navigating_movie(call: CallbackQuery) -> None:
    """Выполняет действия навигационных клавиш"""
    if call.data == 'add_favorites':
        number_movies = checking_number_movies(id_person=call.from_user.id)
        if number_movies:
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                add_favourites(id_person=call.from_user.id,
                               nickname_person=call.from_user.username,
                               movie=data['info_movie'])
            bot.send_message(call.from_user.id, text='Добавил в фильмотеку')
        else:
            bot.send_message(call.from_user.id, text='Список полон. Можно добавить только 5 позиций в избранное.')
    elif call.data == 'del_movie_db':
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            delete_favorite(id_person=call.from_user.id,
                            id_movie=data.get('info_movie').get('id'))
        bot.send_message(call.from_user.id, text='Удалил из фильмотеки')
    elif call.data == 'random':
        random_movie(call)
    elif call.data == 'back_favourites':
        print_favourites(call)
    elif call.data == 'again':
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            pages = data.get('result_search').get('pages')
            page = data.get('result_search').get('page')
            if page == pages:
                bot.send_message(call.from_user.id, text='По этому запросу больше нет фильмов')
            else:
                page += 1
                result = get_movie(title_type=data.get('title_type'),
                                   genre=data.get('genre'),
                                   year=data.get('year'),
                                   rating_kp=data.get('rating_kp'),
                                   limit='5',
                                   page=page)
                data['result_search'] = result
                bot.edit_message_reply_markup(call.message.chat.id,
                                              call.message.id,
                                              reply_markup=output_movie_names(data['result_search'], data['from_is']))
    else:
        print_movies(call)
