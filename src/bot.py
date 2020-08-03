from telebot import TeleBot

from models import Chat, ChatUserProfile, ProfileTransaction
from settings import TELEBOT_TOKEN, DEFAULT_SCORE, DEFAULT_ISSUER
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
    profile.change_score(DEFAULT_SCORE, DEFAULT_ISSUER, {'date': message.date})
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
    profiles = chat.get_profiles(order_by=tuple('-current_score'))
    profile_infos = []
    for profile in profiles:
        profile_infos.append(
            f'@{profile.tg_username}: {profile.current_score}' if profile.tg_username
            else f'{profile.tg_full_name}: {profile.current_score}'
        )
    bot.reply_to(message, _('Current Social Credit scores are:\n{profile_infos}').format(profile_infos='\n'.join(profile_infos)))

@bot.message_handler(commands=['social_credit_help'])
def get_help(message):
    bot.reply_to(message, _('''I am a control bot of Social Credit Score system for Telegram group chats.
Social Credit Score is manipulated via replies to rankable messages, using this sticker set: https://t.me/addstickers/PoohSocialCredit.
Before use, Social Credit System must be enabled for your chat by a Chat Admin, using /social_credit_enable command.
Then, chat members can enroll to Social Credit System using /social_credit_enroll command.
After enrolling, each member has a {start_score} Starting Credit Score.
/social_credit_myscore shows your current Social Credit score, while /social_credit_chatinfo command show score info on everyone enrolled into system in this chat.
/social_credit_help displays this message again.''').format(start_score=DEFAULT_SCORE))
