from telebot import TeleBot
from mongoengine import ValidationError, FieldDoesNotExist

from models import Chat, ChatUserProfile, ProfileTransaction
from settings import TELEBOT_TOKEN, DEFAULT_SCORE, DEFAULT_ISSUER, DEFAULT_VERBOSITY
from handler_validators import change_score_validator
from transactions import TRANSACTIONS
from utils import translate as _


bot = TeleBot(TELEBOT_TOKEN)

@bot.message_handler(content_types=['sticker'], func=change_score_validator)
def change_score(message):
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    issuer_user_id = message.from_user.id
    chat = Chat.objects(tg_chat_id=chat_id).first()
    if not chat:
        bot.reply_to(message, _('Chat is not registered in Social Credit system'))
        return
    profile = ChatUserProfile.objects(chat=chat, tg_user_id=user_id).first()
    issuer_profile = ChatUserProfile.objects(chat=chat, tg_user_id=issuer_user_id).first()
    if profile == issuer_profile:
        bot.reply_to(message, _('Ranking your own messages is not allowed'))
        return
    if not profile:
        bot.reply_to(message, _('Profile is not enrolled in Social Credit system'))
        return
    if not issuer_profile:
        bot.reply_to(message, _('Your profile is not enrolled in Social Credit system'))
        return
    if ProfileTransaction.objects(message__message_id=message.reply_to_message.message_id, issuer=issuer_profile).first():
        bot.reply_to(message, _('You have already ranked this message'))
        return
    transaction = TRANSACTIONS[message.sticker.emoji]
    profile.change_score(
        score_delta=transaction.amount,
        issuer=issuer_profile,
        message=message.reply_to_message.json,
    )
    if chat.verbosity > 1:
        bot.reply_to(message, _(transaction.message_template).format(
            username=f'@{profile.tg_username}' if profile.tg_username else profile.tg_full_name, score=profile.current_score
        ))

@bot.message_handler(commands=['social_credit_enable'])
def register_chat(message):
    chat_id = message.chat.id
    if Chat.objects(tg_chat_id=chat_id).first():
        bot.reply_to(message, _('Chat is already registered in Social Credit system'))
        return
    user_id = message.from_user.id
    admin_ids = map(lambda admin: admin.user.id, bot.get_chat_administrators(chat_id))
    if user_id not in admin_ids:
        bot.reply_to(message, _('You need to be a Chat Admin to register chat in Social Credit system'))
        return
    Chat(tg_chat_id=chat_id).save()
    bot.reply_to(message, _('Chat is sucessfully registered in Social Credit system'))

@bot.message_handler(commands=['social_credit_enroll'])
def create_profile(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat = Chat.objects(tg_chat_id=chat_id).first()
    if not chat:
        bot.reply_to(message, _('Chat is not registered in Social Credit system'))
        return
    if ChatUserProfile.objects(chat=chat, tg_user_id=user_id).first():
        bot.reply_to(message, _('You are already enrolled in Social Credit system'))
        return
    profile = ChatUserProfile(
        chat=chat,
        tg_user_id=user_id,
        tg_first_name=message.from_user.first_name,
        tg_last_name=message.from_user.last_name,
        tg_username=message.from_user.username,
    )
    profile.save()
    profile.change_score(chat.starting_score, DEFAULT_ISSUER, {'date': message.date})
    bot.reply_to(message, _('You have successfully enrolled in Social Credit system'))

@bot.message_handler(commands=['social_credit_myscore'])
def get_profile_score(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat = Chat.objects(tg_chat_id=chat_id).first()
    if not chat:
        bot.reply_to(message, _('Chat is not registered in Social Credit system'))
        return
    profile = ChatUserProfile.objects(chat=chat, tg_user_id=user_id).first()
    if not profile:
        bot.reply_to(message, _('You are not enrolled in Social Credit system'))
        return
    bot.reply_to(message, _('Your Social Credit score is {score}').format(score=profile.current_score))

@bot.message_handler(commands=['social_credit_chatinfo'])
def get_chat_info(message):
    chat = Chat.objects(tg_chat_id=message.chat.id).first()
    if not chat:
        bot.reply_to(message, _('Chat is not registered in Social Credit system'))
        return
    profiles = chat.get_profiles(order_by=('-current_score',))
    profile_infos = []
    for profile in profiles:
        profile_infos.append(
            f'@{profile.tg_username}: {profile.current_score}' if profile.tg_username
            else f'{profile.tg_full_name}: {profile.current_score}'
        )
    bot.reply_to(message, _('Current Social Credit scores are:\n{profile_infos}').format(profile_infos='\n'.join(profile_infos)))

@bot.message_handler(commands=['social_credit_help'])
def get_help(message):
    chat = Chat.objects(tg_chat_id=message.chat.id).first()
    start_score = chat.starting_score if chat else DEFAULT_SCORE
    bot.reply_to(message, _('''I am a control bot of Social Credit Score system for Telegram group chats.
Social Credit Score is manipulated via replies to rankable messages, using this sticker set: https://t.me/addstickers/PoohSocialCredit.
Before use, Social Credit System must be enabled for your chat by a Chat Admin, using /social_credit_enable command.
Then, chat members can enroll to Social Credit System using /social_credit_enroll command.
After enrolling, each member has a {start_score} Starting Credit Score (This can be changed by an admin).
/social_credit_myscore shows your current Social Credit score, while /social_credit_chatinfo command show score info on everyone enrolled into system in this chat.
Admins can get help on admin commands using /social_credit_admin_help.
/social_credit_help displays this message again.''').format(start_score=start_score))

@bot.message_handler(commands=['social_credit_admin_help'])
def get_admin_help(message):
    chat = Chat.objects(tg_chat_id=message.chat.id).first()
    if not chat:
        bot.reply_to(message, _('Chat is not registered in Social Credit system'))
        return
    user_id = message.from_user.id
    admin_ids = map(lambda admin: admin.user.id, bot.get_chat_administrators(message.chat.id))
    if user_id not in admin_ids:
        bot.reply_to(message, _('You need to be a Chat Admin to get Admin help'))
        return
    bot.reply_to(message, _('''Admin can use following commands:
    * /social_credit_enable - enables Social Credit System for this chat
    * /social_credit_set_chat_option - set a value for a chat option. Takes 2 params: option_name and option value, separated by spaces. Example: `/social_credit_set_chat_option starting_score 300`
    
Avaliable chat options:
    * starting_score - starting score for anyone, who enrolls to Social Credit System. Default is {start_score}
    * verbosity - bot verbosity level. Can be 0 - answer only to commands, 1 - allow periodical messages (unused for now), 2 - allow bot reactions. Default is {verbosity}''').format(
        start_score=DEFAULT_SCORE,
        verbosity=DEFAULT_VERBOSITY,
    ))

@bot.message_handler(commands=['social_credit_set_chat_option'])
def set_chat_option(message):
    chat = Chat.objects(tg_chat_id=message.chat.id).first()
    if not chat:
        bot.reply_to(message, _('Chat is not registered in Social Credit system'))
        return
    user_id = message.from_user.id
    admin_ids = map(lambda admin: admin.user.id, bot.get_chat_administrators(message.chat.id))
    if user_id not in admin_ids:
        bot.reply_to(message, _('You need to be a Chat Admin to set chat options'))
        return
    command_params = message.text.split(' ')[1:]
    if len(command_params) < 2:
        bot.reply_to(message, _('Invalid command parameters. Use /social_credit_admin_help for details.'))
        return
    option, value = command_params
    try:
        chat.set_option(option, value)
    except ValidationError as e:
        error_message = _(e._format_errors().split(':')[0])
        bot.reply_to(message, _('Invalid value for option {option}: {error_message}').format(
            option=option,
            error_message=error_message,
        ))
        return
    except FieldDoesNotExist:
        bot.reply_to(message, _('Unknown option {option}').format(option=option))
        return
    bot.reply_to(message, _('Option {option} set to {value}').format(
        option=option,
        value=value,
    ))
