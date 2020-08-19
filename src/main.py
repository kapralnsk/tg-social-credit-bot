from logging import getLogger
from mongoengine import connect

from bot import bot
from translator import Translator
from settings import MONGO_CONNECTION_STRING
from logger import setup_logger
import social_credit_routes # TODO refine routing module loading


setup_logger()
logger = getLogger('social_credit')
db_client = connect('social_credit', host=MONGO_CONNECTION_STRING)
# check mongo connection after creating client
# no exception catching: if mongo is unavailable - we want to crash
# According to pymongo doc: The ismaster command is cheap and does not require auth.
db_client.admin.command('ismaster')
bot.translator = Translator()
logger.info('bot started')
bot.polling()
