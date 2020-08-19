from bot import bot
from settings import DEFAULT_LANGUAGE
from exceptions import SocialCreditError

from .handler import PenisHandler


def handle(message, method_name, allow_no_chat=False):
    try:
        handler = PenisHandler(bot, message, allow_no_chat=allow_no_chat)
    except SocialCreditError as e:
        text = bot.translator.translate(str(e), DEFAULT_LANGUAGE)
        bot.reply_to(message, text)
        return
    try:
        method = getattr(handler, method_name)
        method()
    except SocialCreditError as e:
        handler.send_system(str(e))
    except Exception as e:
        logger.exception(str(e))
        bot.reply_to(message, "I've done goofed")

@bot.message_handler(commands=['social_credit_chat_penises'])
def get_chat_penises(message):
    handle(message, 'get_chat_penises')
