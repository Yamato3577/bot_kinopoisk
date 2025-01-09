from telebot.types import Message
from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    """Отвечает на сообщения без состояния"""
    bot.reply_to(message, "Выберете команду из меню")
