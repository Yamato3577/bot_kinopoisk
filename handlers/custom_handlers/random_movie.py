from loguru import logger

from typing import Union
from telebot.types import Message, CallbackQuery


from handlers.custom_handlers.info_movie import print_info_movie
from loader import bot
from requests_api.kinopoisk import get_random_movie
from states.user_states import UserInfoState


@bot.message_handler(state='*', commands=['random_movie'])
def random_movie(message: Union[Message, CallbackQuery]) -> None:
    """Вывод случайного фильма"""
    if type(message).__name__ == 'Message':
        chat_id = message.chat.id
    else:
        chat_id = message.message.chat.id
    bot.set_state(message.from_user.id, UserInfoState.random_movie, chat_id)
    logger.info('Пользователь {}, запросил случайный фильм', message.from_user.id)
    movie = get_random_movie()
    if movie:
        with bot.retrieve_data(message.from_user.id, chat_id) as data:
            data['info_movie'] = print_info_movie(message=message, movie=movie, from_is='random')
    else:
        bot.send_message(message.from_user.id, 'Ничего не найдено, попробуйте снова')
        bot.delete_state(message.from_user.id)

