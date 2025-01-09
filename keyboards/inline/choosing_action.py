from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.CRUD import checking_movie
from utils.smiles import smile_repeat, smile_save, smile_back, smile_del


def choosing_action(id_user: int, id_movie: int, from_is: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора действия, после вывода информации о фильме.
    Сначала проверяет наличие фильма в БД (Избранное), потом формируются кнопки,
    в зависимости от куда вызывается клавиатура.
    :param id_user: int
    :param id_movie: int
    :param from_is: str
    Указывает от куда вызывается клавиатура.
    :return: InlineKeyboardMarkup
    """
    check = checking_movie(id_user, id_movie)
    markup = InlineKeyboardMarkup()
    if from_is == 'random':
        if check:
            markup.add(InlineKeyboardButton(text=f'{smile_repeat} Еще раз {smile_repeat}', callback_data='random'),
                       InlineKeyboardButton(text='Уже в коллекции', callback_data='None'))
        else:
            markup.add(InlineKeyboardButton(text=f'{smile_repeat} Еще раз {smile_repeat}', callback_data='random'),
                       InlineKeyboardButton(text=f'{smile_save} Сохранить', callback_data='add_favorites'))

    if from_is == 'favourites':
        markup.add(InlineKeyboardButton(text=f'{smile_back} Назад', callback_data='back_favourites'),
                   InlineKeyboardButton(text=f'{smile_del} Удалить', callback_data='del_movie_db'))

    if from_is in ['search_name', 'search_param']:
        if check:
            markup.add(InlineKeyboardButton(text=f'{smile_back} Назад', callback_data='back_movies'),
                       InlineKeyboardButton(text='Уже в коллекции', callback_data='None'))
        else:
            markup.add(InlineKeyboardButton(text=f'{smile_back} Назад', callback_data='back_movies'),
                       InlineKeyboardButton(text=f'{smile_save} Сохранить', callback_data='add_favorites'))

    return markup
