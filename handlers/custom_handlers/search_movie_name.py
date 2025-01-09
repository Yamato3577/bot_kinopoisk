from telebot.types import Message

from loguru import logger

from keyboards.inline.movies import output_movie_names
from loader import bot
from requests_api.kinopoisk import get_movie
from states.user_states import UserInfoState


@bot.message_handler(state='*', commands=['search_movie_name'])
def typing_name(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Введите название')
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)


@bot.message_handler(state=UserInfoState.name)
def get_movie_print_info(message: Message) -> None:
    """Поиск фильма по названию и вывод клавиатуры-списка фильмов"""
    logger.info('Пользователь {}, ввел фильм: {}', message.from_user.username, message.text)
    result = get_movie(name=message.text)
    if result:
        bot.set_state(message.from_user.id, UserInfoState.temp, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['result_search'] = result
            data['from_is'] = 'search_name'
            bot.send_message(message.from_user.id, 'Найденные фильмы:',
                             reply_markup=output_movie_names(data['result_search']))
    else:
        bot.send_message(message.from_user.id, 'Ничего не найдено, выберите команду из меню')
        bot.delete_state(message.from_user.id, message.chat.id)
