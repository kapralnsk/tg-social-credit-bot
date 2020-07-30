from settings import SOCIAL_CREDIT_STICKERPACK_NAME


def change_score_validator(message):
    """
    message can be a Social Credit Transaction if:
    * it is a reply to another message
    * reply is a sticker from PoohSocialCredit pack
    """
    # content type in message_handler decorator does not filter non-sticker messages :(
    if message.content_type != 'sticker':
        return False
    is_reply = message.reply_to_message is not None
    is_social_credit_stickerpack = message.sticker.set_name == SOCIAL_CREDIT_STICKERPACK_NAME
    return is_reply and is_social_credit_stickerpack
