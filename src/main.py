from mongoengine import connect

from bot import bot
from settings import MONGO_CONNECTION_STRING


db_client = connect('social_credit', host=MONGO_CONNECTION_STRING)
# check mongo connection after creating client
# no exception catching: if mongo is unavailable - we want to crash
# According to pymongo doc: The ismaster command is cheap and does not require auth.
db_client.admin.command('ismaster')
print('bot started')
bot.polling()
