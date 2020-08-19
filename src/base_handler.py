from models import Chat, ChatUserProfile, ProfileTransaction
from settings import DEFAULT_VERBOSITY, DEFAULT_LANGUAGE
import exceptions

class BaseHandler(object):
    def __init__(self, bot, message=None, chat=None, allow_no_chat=False):
        if not message and not chat:
            raise ValueError('Handler must be initialized with either message or chat.')
        self.bot = bot
        self.message = message
        if not message:
            # then we must have chat
            self.chat = chat
        else:
            # then we need to find chat in DB
            try:
                self.chat = self.get_chat()
            except exceptions.SocialCreditError as e:
                if allow_no_chat:
                    self.chat = None
                else:
                    raise e

    @staticmethod
    def run_validators(validators):
        def decorator(func):
            def wrapper(handler):
                for validator in validators:
                    validator(handler)
                func(handler)
            return wrapper
        return decorator


    def _get_wrapper(self, model, query, error_message):
        try:
            return model.objects.get(**query)
        except model.DoesNotExist:
            raise exceptions.SocialCreditError(error_message)

    def _get_chat_verbosity(self):
        return self.chat.verbosity if self.chat else DEFAULT_VERBOSITY

    def _get_chat_lang(self):
        return self.chat.language if self.chat else DEFAULT_LANGUAGE 
        
    def get_chat(self):
        return self._get_wrapper(
            Chat,
            {'tg_chat_id': self.message.chat.id},
            'Chat is not registered in Social Credit system',
        )
    
    def get_profile(self):
        return self._get_wrapper(
            ChatUserProfile,
            {'chat': self.chat, 'tg_user_id': self.message.from_user.id},
            'You are not enrolled in Social Credit system',
        )

    def get_assessed_profile(self):
        return self._get_wrapper(
            ChatUserProfile,
            {'chat': self.chat, 'tg_user_id': self.message.reply_to_message.from_user.id},
            'Profile is not enrolled in Social Credit system',
        )

    def send_system(self, text, str_format={}):
        language = self._get_chat_lang()
        translated = self.bot.translator.translate(text, language)
        if str_format:
            translated = translated.format(**str_format)
        self.bot.reply_to(self.message, translated)

    def send_periodical(self, text, str_format={}):
        language = self._get_chat_lang()
        chat_verbosity = self._get_chat_verbosity()
        periodical_verbosity = 1
        if chat_verbosity >= periodical_verbosity:
            translated = self.bot.translator.translate(text, language)
            if str_format:
                translated = translated.format(**str_format)
            if self.message:
                self.bot.reply_to(self.message, translated)
            else:
                self.bot.send_message(self.chat.tg_chat_id, translated)

    def send_reaction(self, text, str_format={}):
        language = self._get_chat_lang()
        chat_verbosity = self._get_chat_verbosity()
        reaction_verbosity = 2
        if chat_verbosity >= reaction_verbosity:
            translated = self.bot.translator.translate(text, language)
            if str_format:
                translated = translated.format(**str_format)
            self.bot.reply_to(self.message, translated)