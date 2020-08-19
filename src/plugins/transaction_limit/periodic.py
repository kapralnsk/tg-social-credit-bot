from logging import getLogger

from mongoengine import DoesNotExist


logger = getLogger('social_credit')

def reset_transactions(task, bot):
    profiles = task.chat.get_profiles()
    try:
        options = task.chat.plugin_options.get(plugin_name='transaction_limit')
    except DoesNotExist as e:
        logger.exception(f'reset transactions error: {str(e)}')
        return
    limit = options.limit
    for profile in profiles:
        options = profile.plugin_options.get(plugin_name='transaction_limit')
        options.transactions_left = limit
        profile.plugin_options.save()
