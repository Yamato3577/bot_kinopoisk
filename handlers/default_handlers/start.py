from telebot.types import Message
from loader import bot
from states.user_states import UserInfoState


@bot.message_handler(state='*', commands=['start'])
def bot_start(message: Message):
    bot.set_state(message.from_user.id, UserInfoState.start, message.chat.id)
    bot.reply_to(message,
                 f'Привет, {message.from_user.full_name}!\n'
                 f'Я бот по поиску фильмов, могу найти что-то интересное и добавить в вашу фильмотеку.\n'
                 f'В меню есть несколько вариантов поиска.\n'
                 f'Могу найти по названию или по параметрам (только вышедшие картины), а если не знаете,'
                 f' что посмотреть, предложу случайный фильм. Также буду хранить вашу фильмотеку,'
                 f' но не забывайте удалять из неё просмотренные картины.\n'
                 f'А теперь приступим! Выберите действие из меню')
    bot.send_sticker(message.chat.id,
                     sticker='CAACAgIAAxkBAAEBqGhlPoAwSGAMLg8Q-K70nrNvcN01HwACrwEAAladvQoEu_codx9SCTAE')
