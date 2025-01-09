from telebot.types import Message, CallbackQuery
from datetime import date

from loguru import logger

from loader import bot
from keyboards.inline.movies import output_movie_names
from keyboards.inline.start_search_by_param import search
from states.user_states import UserInfoState
from requests_api.kinopoisk import get_movie
from keyboards.inline.category import category_keyboard
from keyboards.inline.genres_keyboard import genres_keyboard_one, genres_keyboard_two, genres_keyboard_three


@bot.message_handler(state='*', commands=['search_movie_param'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.category, message.chat.id)
    bot.send_message(message.from_user.id, 'Выберите категорию:', reply_markup=category_keyboard())


@bot.callback_query_handler(func=lambda call: call.data in ['movie', 'tv-series'])
def callback_category(call: CallbackQuery) -> None:
    if call:
        bot.answer_callback_query(call.id, text=f'Вы выбрали {call.data}')
        bot.edit_message_text('Выберите жанр: ', call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=genres_keyboard_one())
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['title_type'] = call.data
        logger.info('Пользователь {}, выбрал категорию: {}', call.from_user.username, call.data)


@bot.callback_query_handler(func=lambda call: call.data in ['боевик', 'триллер', 'комедия', 'ужасы',
                                                            'фантастика', 'фэнтези', 'next_two',
                                                            'приключения', 'история', 'вестерн', 'драма',
                                                            'мелодрама', 'детектив', 'back_one', 'next_three',
                                                            'военный', 'биография', 'семейный', 'мюзикл',
                                                            'мультфильм', 'аниме', 'back_two'
                                                            ])
def callback_genres(call: CallbackQuery) -> None:
    if call:
        if call.data == 'back_one':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=genres_keyboard_one())
        elif call.data in ['next_two', 'back_two']:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=genres_keyboard_two())
        elif call.data == 'next_three':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=genres_keyboard_three())
        else:
            bot.answer_callback_query(call.id, text=f'Вы выбрали {call.data}')
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                if call.data == 'мультфильм':
                    if data['title_type'] == 'tv-series':
                        data['title_type'] = 'animated-series'
                    else:
                        data['title_type'] = 'cartoon'
                elif call.data == 'аниме':
                    data['title_type'] = 'anime'
                data['genre'] = call.data
            bot.set_state(call.from_user.id, UserInfoState.year, call.message.chat.id)
            bot.send_message(call.from_user.id, f'Введите год выпуска (2003)\n'
                                                f'или период выпуска (1940-{date.today().year})')
            logger.info('Пользователь {}, выбрал жанр: {}', call.from_user.username, call.data)


@bot.message_handler(state=UserInfoState.year)
def get_year(message: Message) -> None:
    now_year = date.today().year
    years = []
    line_data = message.text.split('-')
    number_line_data = len(line_data)
    if number_line_data < 3:
        for number, year in enumerate(line_data):
            clear_year = year.strip()
            if not clear_year.isdigit():
                bot.send_message(message.from_user.id, f'Ошибка в {number+1} дате.'
                                                       f' Дата может состоять только из цифр.\n'
                                                       f'Введите дату заново')
            elif len(clear_year) != 4:
                bot.send_message(message.from_user.id, f'Ошибка в {number + 1} дате.' 
                                                       f' Дата должна быть четырехзначная.\n'
                                                       f'Введите дату заново')
            elif (int(clear_year) < 1940) or (int(clear_year) > now_year):
                bot.send_message(message.from_user.id, f'Ошибка в {number + 1} значении.' 
                                                       f'Год должен быть периодом\n от 1940 до {now_year}.\n'
                                                       f'Введите  заново')
            else:
                years.append(clear_year)
        number_years = len(years)
        if number_line_data == number_years:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['year'] = '-'.join(sorted(years))
            bot.send_message(message.from_user.id, 'Введите рейтинг по "КиноПоиску" периодом (1-10)')
            bot.set_state(message.from_user.id, UserInfoState.rating_kp)
            logger.info('Пользователь {}, выбрал год: {}', message.from_user.username, data['year'])
    else:
        bot.send_message(message.from_user.id, 'Не правильно введены данные, введите заново')


@bot.message_handler(state=UserInfoState.rating_kp)
def get_rating(message: Message) -> None:
    ratings = []
    translation_type = {'movie': 'Фильм', 'tv-series': 'Сериал', 'cartoon': 'Мультфильм',
                        'anime': 'Аниме', 'animated-series': 'Мультсериал'}
    line_data = message.text.split('-')
    if len(line_data) == 2:
        for number, rating in enumerate(line_data):
            clear_rating = rating.strip()
            if not clear_rating.isdigit():
                bot.send_message(message.from_user.id, f'Ошибка в {number+1} значении.'
                                                       f'Рейтинг должен состоять только из целых цифр.\n'
                                                       f'Введите заново')
            elif (int(clear_rating) < 1) or (int(clear_rating) > 10):
                bot.send_message(message.from_user.id, f'Ошибка в {number + 1} значении.' 
                                                       f'Рейтинг должен быть периодом (1-10).\n'
                                                       f'Введите  заново')
            else:
                ratings.append(int(clear_rating))
        if len(ratings) == 2:
            ratings = [str(number) for number in sorted(ratings)]
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['rating_kp'] = '-'.join(ratings)
                logger.info('Пользователь {}, выбрал рейтинг: {}', message.from_user.username, data['rating_kp'])
                bot.set_state(message.from_user.id, UserInfoState.temp, message.chat.id)
                bot.send_message(message.from_user.id,
                                 (f'Собранные данные:\n'
                                  f'Тип: {translation_type[data["title_type"]]}\n'
                                  f'Жанр: {data["genre"]}\n'
                                  f'Год: {data["year"]}\n'
                                  f'Рейтинг на КП: {data["rating_kp"]}'),
                                 reply_markup=search())

                result = get_movie(title_type=data.get('title_type'),
                                   genre=data.get('genre'),
                                   year=data.get('year'),
                                   rating_kp=data.get('rating_kp'),
                                   limit='5',
                                   page=1)
                data['result_search'] = result
                data['from_is'] = 'search_param'
    else:
        bot.send_message(message.from_user.id, 'Не правильно введены данные, введите заново.'
                                               ' Рейтинг должен быть периодом (1-10)')


@bot.callback_query_handler(func=lambda call: call.data in ['search'])
def print_movies(call: CallbackQuery) -> None:
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        if data['result_search']:
            bot.send_message(call.from_user.id, 'Найденные фильмы:',
                             reply_markup=output_movie_names(data['result_search'], data['from_is']))
        else:
            bot.send_message(call.from_user.id, 'С данными параметрами нет фильмов. Выберите другие параметры.')
