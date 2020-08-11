import gettext
import os


class Translator(object):
    def __init__(self):
        langdir = os.path.join(os.getcwd(), 'locale')
        self.translations = {}
        for lang in os.listdir(langdir):
            self.translations[lang] = gettext.translation(
                'tg-social-credit-bot',
                langdir,
                languages=[lang],
            )
        
    def translate(self, text, lang):
        return self.translations[lang].gettext(text)

    @property
    def languages(self):
        return ('en', *self.translations.keys())
