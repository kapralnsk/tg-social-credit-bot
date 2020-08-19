from datetime import time

from mongoengine import DoesNotExist
from pytz import UTC

from models import ChatPeriodicTask
from exceptions import SocialCreditError

from .periodic import *


DEFAULT_TIME = time(hour=17, tzinfo=UTC)
HELP_TEXT = "Automatically sends leaderboard (`/social_credit_chatinfo` command) every day, at {time} o'clock UTC."

def enable(chat):
    try:
        options = chat.plugin_options.get(plugin_name='chatinfo')
    except DoesNotExist:
        pass
    else:
        raise SocialCreditError('Plugin is already enabled.')
    chat.plugin_options.create(plugin_name='chatinfo')
    chat.plugin_options.save()
    ChatPeriodicTask(
        chat=chat,
        plugin_name='chatinfo',
        module='post_chat_info',
        time=DEFAULT_TIME,
    ).save()


def disable(chat):
    try:
        options = chat.plugin_options.get(plugin_name='chatinfo')
    except DoesNotExist:
        raise SocialCreditError('Plugin is already disabled.')
    chat.plugin_options.remove(options)
    chat.plugin_options.save()
    ChatPeriodicTask.objects.get(
        chat=chat,
        plugin_name='chatinfo',
        module='post_chat_info',
    ).delete()

def get_help():
    return HELP_TEXT, {'time': DEFAULT_TIME.hour}
