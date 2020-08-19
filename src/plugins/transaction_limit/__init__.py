from datetime import time

from mongoengine import DoesNotExist
from pytz import UTC

from models import ChatPeriodicTask
from exceptions import SocialCreditError

from .options import TransactionLimitChatOptions, TransactionLimitProfileOptions
from .signals import *
from .periodic import *


DEFAULT_TIME = time(hour=17, tzinfo=UTC)
DEFAULT_LIMIT = 10
HELP_TEXT = '''Implements daily transaction limit: any profile can rank only limited number of messages a day.
Default limit is {limit}, resets every day at {time} o'clock UTC.'''
# TODO add following to help text, when set_plugin_option goes public
# Available options:
# * limit - changes transaction limit for everyone in the chat. Applies, when limit is reset.'''

def enable(chat):
    try:
        options = chat.plugin_options.get(plugin_name='transaction_limit')
    except DoesNotExist:
        pass
    else:
        raise SocialCreditError('Plugin is already enabled.')
    chat_options = TransactionLimitChatOptions(plugin_name='transaction_limit', limit=DEFAULT_LIMIT)
    profiles = chat.get_profiles()
    chat.plugin_options.append(chat_options)
    chat.plugin_options.save()
    for profile in profiles:
        profile_option = TransactionLimitProfileOptions(plugin_name='transaction_limit', transactions_left=DEFAULT_LIMIT)
        profile.plugin_options.append(profile_option)
        profile.plugin_options.save()
    ChatPeriodicTask(
        chat=chat,
        plugin_name='transaction_limit',
        module='reset_transactions',
        time=DEFAULT_TIME,
    ).save()


def disable(chat):
    try:
        options = chat.plugin_options.get(plugin_name='transaction_limit')
    except DoesNotExist:
        raise SocialCreditError('Plugin is already disabled.')
    profiles = chat.get_profiles()
    chat.plugin_options.remove(options)
    chat.plugin_options.save()
    for profile in profiles:
        profile_options = profile.plugin_options.get(plugin_name='transaction_limit')
        profile.plugin_options.remove(profile_options)
        profile.plugin_options.save()
    
    ChatPeriodicTask.objects.get(
        chat=chat,
        plugin_name='transaction_limit',
        module='reset_transactions',
    ).delete()
    

def get_help():
    return HELP_TEXT, {'time': DEFAULT_TIME.hour, 'limit': DEFAULT_LIMIT}
