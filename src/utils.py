import gettext
import os


def translate(text, language='RU'):
    return gettext.translation(
        'tg-social-credit-bot',
        os.path.join(os.getcwd(), 'locale'),
        languages=[language],
        fallback=True,
    ).gettext(text)
    