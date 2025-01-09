from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot
from states.user_states import UserInfoState


@bot.message_handler(state='*', commands=['help'])
def bot_help(message: Message):
    """Выводит справку об основных командах бота."""
    bot.set_state(message.from_user.id, UserInfoState.help, message.chat.id)
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
