from collections import namedtuple

import mongoengine

import exceptions
import message_validators
from base_handler import BaseHandler
from settings import DEFAULT_ISSUER, DEFAULT_SCORE, DEFAULT_VERBOSITY, DEFAULT_LANGUAGE
from models import Chat, ChatUserProfile, ProfileTransaction


Transaction = namedtuple('Transaction', 'amount message_template')

class SocialCreditHandler(BaseHandler):
    TRANSACTIONS = {
        '😄': Transaction(20, 'Good! {username} Social Credit Score is now {score}'),
        '😞': Transaction(-20, 'Public shame! {username} Social Credit Score is now {score}'),
    }

    def change_score(self):
        assessed_profile = self.get_assessed_profile()
        issuer_profile = self.get_profile()
        if assessed_profile == issuer_profile:
            raise exceptions.SocialCreditError('Ranking your own messages is not allowed')
        # TODO put message_id as a top-level param in Transaction,
        # bind it together with issuer as an UniqueTogether,
        # then remove this check
        if ProfileTransaction.objects(
            message__message_id=self.message.reply_to_message.message_id,
            issuer=issuer_profile).first():
            raise exceptions.SocialCreditError('You have already ranked this message')
        transaction = self.TRANSACTIONS[self.message.sticker.emoji]
        assessed_profile.change_score(
            score_delta=transaction.amount,
            issuer=issuer_profile,
            message=self.message.reply_to_message.json,
        )
        reaction = transaction.message_template
        self.send_reaction(reaction, str_format={
            'username': f'@{assessed_profile.tg_username}' if assessed_profile.tg_username else assessed_profile.tg_full_name,
            'score': assessed_profile.current_score,
        })

    @BaseHandler.run_validators([
        message_validators.validate_chat_not_exist,
        message_validators.validate_user_is_admin,
    ])
    def register_chat(self):
        self.chat = Chat(tg_chat_id=self.message.chat.id).save()
        self.send_system('Chat is sucessfully registered in Social Credit system')

    @BaseHandler.run_validators([message_validators.validate_profile_does_not_exist])
    def create_profile(self):
        user_id = self.message.from_user.id
        profile = ChatUserProfile(
            chat=self.chat,
            tg_user_id=self.message.from_user.id,
            tg_first_name=self.message.from_user.first_name,
            tg_last_name=self.message.from_user.last_name,
            tg_username=self.message.from_user.username,
        )
        profile.save()
        profile.change_score(self.chat.starting_score, DEFAULT_ISSUER, {'date': self.message.date})
        self.send_system('You have successfully enrolled in Social Credit system')

    @BaseHandler.run_validators([message_validators.validate_profile_exist])
    def get_profile_score(self):
        profile = self.get_profile()
        user_id = self.message.from_user.id
        self.send_system(
            'Your Social Credit score is {score}',
            str_format={'score': profile.current_score},
        )

    def get_chat_info(self):
        profiles = self.chat.get_profiles(order_by=('-current_score',))
        profile_infos = []
        for profile in profiles:
            profile_infos.append(
                f'@{profile.tg_username}: {profile.current_score}' if profile.tg_username
                else f'{profile.tg_full_name}: {profile.current_score}'
            )
        self.send_system(
            'Current Social Credit scores are:\n{profile_infos}',
            str_format={'profile_infos': '\n'.join(profile_infos)},
        )

    def get_help(self):
        start_score = self.chat.starting_score if self.chat else DEFAULT_SCORE
        self.send_system(
            '''I am a control bot of Social Credit Score system for Telegram group chats.
Social Credit Score is manipulated via replies to rankable messages, using this sticker set: https://t.me/addstickers/PoohSocialCredit.
Before use, Social Credit System must be enabled for your chat by a Chat Admin, using /social_credit_enable command.
Then, chat members can enroll to Social Credit System using /social_credit_enroll command.
After enrolling, each member has a {start_score} Starting Credit Score (This can be changed by an admin).
/social_credit_myscore shows your current Social Credit score, while /social_credit_chatinfo command show score info on everyone enrolled into system in this chat.
Admins can get help on admin commands using /social_credit_admin_help.
/social_credit_help displays this message again.''',
            str_format={'start_score': start_score},
        )

    @BaseHandler.run_validators([message_validators.validate_user_is_admin])
    def get_admin_help(self):
        languages = ', '.join(self.bot.translator.languages)
        self.send_system(
            '''Admin can use following commands:
    * /social_credit_enable - enables Social Credit System for this chat
    * /social_credit_set_chat_option - set a value for a chat option. Takes 2 params: option_name and option value, separated by spaces. Example: `/social_credit_set_chat_option starting_score 300`
    
Avaliable chat options:
    * starting_score - starting score for anyone, who enrolls to Social Credit System. Default is {start_score}
    * verbosity - bot verbosity level. Can be 0 - answer only to commands, 1 - allow periodical messages (unused for now), 2 - allow bot reactions. Default is {verbosity}
    * language - bot messages language. Available languages are {languages}. Default is `{language}`, however this can fallback to `en`''',
            str_format={'start_score': DEFAULT_SCORE, 'verbosity': DEFAULT_VERBOSITY, 'language': DEFAULT_LANGUAGE, 'languages': languages}
        )

    @BaseHandler.run_validators([
        message_validators.validate_user_is_admin,
        message_validators.validate_chat_option,
    ])
    def set_chat_option(self):
        option, value = self.message.text.split(' ')[1:]
        try:
            self.chat.set_option(option, value)
        except mongoengine.ValidationError as e:
            error_message = e._format_errors().split(':')[0]
            # TODO refine translation process of those kind of exceptions
            # (where template is translated first, and then formatting is applied).
            # Handler logic shouldn't worry about translations 
            raise exceptions.SocialCreditError(
                'Invalid value for option {option}: {error_message}'.format(option=option, error_message=error_message),
            )
        except mongoengine.FieldDoesNotExist:
            raise exceptions.SocialCreditError(
                'Unknown option {option}'.format(option=option)
            )
        self.send_system(
            'Option {option} set to {value}',
            str_format={'option': option, 'value': value}
        )