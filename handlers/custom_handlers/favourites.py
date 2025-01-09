from typing import Union
from telebot.types import Message, CallbackQuery

from database.CRUD import get_favourites, checking_movie
from keyboards.inline.movies import output_movie_names
from loader import bot
from states.user_states import UserInfoState


@bot.message_handler(state='*', commands=['favourites'])
def print_favourites(message: Union[Message, CallbackQuery]) -> None:
    """Проверяет наличие фильмов в БД и выводит их список"""
    check = checking_movie(id_person=message.from_user.id)
    bot.set_state(message.from_user.id, UserInfoState.favourites)
    if check:
        my_movies = get_favourites(message.from_user.id)
        with bot.retrieve_data(message.from_user.id) as data:
            data['result_search'] = my_movies
            data['from_is'] = 'favourites'
        bot.send_message(message.from_user.id, 'Избранное:', reply_markup=output_movie_names(my_movies))
    else:
        bot.send_message(message.from_user.id, 'Здесь пусто, добавьте фильмы')
