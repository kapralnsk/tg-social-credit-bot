import exceptions
from models import ChatUserProfile, ProfileTransaction

def validate_chat_not_exist(handler):
    if handler.chat:
        raise exceptions.SocialCreditError('Chat is already registered in Social Credit system')

def validate_user_is_admin(handler):
    user_id = handler.message.from_user.id
    chat_id = handler.message.chat.id
    admin_ids = map(lambda admin: admin.user.id, handler.bot.get_chat_administrators(chat_id))
    if user_id not in admin_ids:
        raise exceptions.SocialCreditError('You need to be a Chat Admin to perform this action')

def validate_profile_does_not_exist(handler):
    chat_id = handler.message.chat.id
    user_id = handler.message.from_user.id
    if ChatUserProfile.objects(chat=chat_id, tg_user_id=user_id).first():
        raise exceptions.SocialCreditError('You are already enrolled in Social Credit system')

def validate_profile_exist(handler):
    chat_id = handler.message.chat.id
    user_id = handler.message.from_user.id
    try:
        ChatUserProfile.objects(chat=chat_id, tg_user_id=user_id).get()
    except ChatUserProfile.DoesNotExist:
        raise exceptions.SocialCreditError('You are not enrolled in Social Credit system')

def validate_chat_option(handler):
    command_params = handler.message.text.split(' ')[1:]
    if len(command_params) < 2:
        raise exceptions.SocialCreditError('Invalid command parameters. Use /social_credit_admin_help for details.')
