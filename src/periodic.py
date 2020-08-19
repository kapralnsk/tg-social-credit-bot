import datetime
from logging import getLogger
from importlib import import_module

from mongoengine import connect
from pytz import UTC

from bot import bot
from models import ChatPeriodicTask
from translator import Translator
from settings import MONGO_CONNECTION_STRING
from logger import setup_logger


def setup():
    bot.translator = Translator()
    db_client = connect('social_credit', host=MONGO_CONNECTION_STRING)
    # check mongo connection after creating client
    # no exception catching: if mongo is unavailable - we want to crash
    # According to pymongo doc: The ismaster command is cheap and does not require auth.
    db_client.admin.command('ismaster')
    setup_logger()

def run_tasks():
    setup()
    logger = getLogger('social_credit')
    logger.info('running periodical tasks')
    time = datetime.datetime.now(tz=UTC).time().replace(second=0, microsecond=0)
    tasks = ChatPeriodicTask.get_scheduled(time=time)
    for task in tasks:
        func = getattr(import_module(f'plugins.{task.plugin_name}'), task.module)
        func(task, bot)

if __name__ == '__main__':
    run_tasks()
