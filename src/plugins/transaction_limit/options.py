from mongoengine import IntField

from models import PluginOptions


class TransactionLimitChatOptions(PluginOptions):
    limit = IntField()

class TransactionLimitProfileOptions(PluginOptions):
    transactions_left = IntField()
