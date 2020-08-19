from social_credit_handler import SocialCreditHandler


def post_chat_info(task, bot):
    handler = SocialCreditHandler(bot=bot, chat=task.chat)
    profile_infos = handler.get_profile_infos()
    handler.send_periodical(
        'Current Social Credit scores are:\n{profile_infos}',
        str_format={'profile_infos': '\n'.join(profile_infos)},
    )
