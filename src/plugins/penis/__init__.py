from mongoengine import DoesNotExist

from exceptions import SocialCreditError

from .routes import *


HELP_TEXT = 'Shows chat leaderboard, but in penises. Use /social_credit_chat_penises to see it.'

def enable(chat):
    try:
        options = chat.plugin_options.get(plugin_name='penis')
    except DoesNotExist:
        pass
    else:
        raise SocialCreditError('Plugin is already enabled.')
    chat.plugin_options.create(plugin_name='penis')
    chat.plugin_options.save()

def disable(chat):
    try:
        options = chat.plugin_options.get(plugin_name='penis')
    except DoesNotExist:
        raise SocialCreditError('Plugin is already disabled.')
    chat.plugin_options.remove(options)
    chat.plugin_options.save()

def get_help():
    return HELP_TEXT, {}