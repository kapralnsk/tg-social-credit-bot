from mongoengine import signals, DoesNotExist

from exceptions import SocialCreditError
from models import ProfileTransaction


def check_limit(sender, document, created):
    issuer = document.issuer
    try:
        options = issuer.plugin_options.get(plugin_name='transaction_limit')
    except DoesNotExist:
        # plugin must be disabled, skipping
        return
    if not options.transactions_left:
        raise SocialCreditError('Transaction limit exceeded.')
    options.transactions_left -= 1
    issuer.plugin_options.save()

signals.pre_save_post_validation.connect(check_limit, sender=ProfileTransaction)
