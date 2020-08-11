from bot import bot
from social_credit_handler import SocialCreditHandler
from handler_validators import change_score_validator
from exceptions import SocialCreditError
from settings import DEFAULT_LANGUAGE

def handle(message, method_name, allow_no_chat=False):
    try:
        handler = SocialCreditHandler(bot, message, allow_no_chat=allow_no_chat)
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
        # TODO add proper logging, and log en error here
        bot.reply_to(message, "I've done goofed")


@bot.message_handler(content_types=['sticker'], func=change_score_validator)
def change_score(message):
    handle(message, 'change_score')

@bot.message_handler(commands=['social_credit_enable'])
def register_chat(message):
    handle(message, 'register_chat', allow_no_chat=True)

@bot.message_handler(commands=['social_credit_enroll'])
def create_profile(message):
    handle(message, 'create_profile')

@bot.message_handler(commands=['social_credit_myscore'])
def get_profile_score(message):
    handle(message, 'get_profile_score')

@bot.message_handler(commands=['social_credit_chatinfo'])
def get_chat_info(message):
    handle(message, 'get_chat_info')

@bot.message_handler(commands=['social_credit_help'])
def get_help(message):
    handle(message, 'get_help', allow_no_chat=True)

@bot.message_handler(commands=['social_credit_admin_help'])
def get_admin_help(message):
    handle(message, 'get_admin_help')

@bot.message_handler(commands=['social_credit_set_chat_option'])
def set_chat_option(message):
    handle(message, 'set_chat_option')