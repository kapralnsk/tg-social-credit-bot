import mongoengine

import model_validators
from settings import DEFAULT_SCORE

CHAT_VERBOSITIES = (
    (0, 'Commands only'),
    (1, 'Periodical messages'),
    (2, 'Reactions'),
)
class Chat(mongoengine.Document):
    PROTECTED_OPTIONS = ['tg_chat_id']
    CHAT_VERBOSITIES = CHAT_VERBOSITIES

    tg_chat_id = mongoengine.IntField(required=True, primary_key=True)
    starting_score = mongoengine.IntField(
        required=True,
        default=DEFAULT_SCORE,
        validation=model_validators.validate_starting_score
    )
    verbosity = mongoengine.IntField(
        required=True,
        choices=CHAT_VERBOSITIES,
        default=CHAT_VERBOSITIES[0][0],
    )

    def clean(self):
        # Choices validation happens before type casting (.to_mongo() call),
        # so we're manually casting it here, before validation.
        # Cool shit MongoEngine.
        if type(self.starting_score) == str:
            try:
                self.starting_score = int(self.starting_score)
            except ValueError:
                pass # let MongoEngine logic handle this error

    def get_profiles(self, order_by=tuple()):
        profiles = ChatUserProfile.objects(chat=self).order_by(*order_by)
        return profiles

    def set_option(self, option, value):
        if option in self.PROTECTED_OPTIONS:
            raise mongoengine.ValidationError
        if option not in self._fields_ordered:
            raise mongoengine.FieldDoesNotExist
        setattr(self, option, value)
        self.save()


class ChatUserProfile(mongoengine.Document):
    chat = mongoengine.ReferenceField(Chat, required=True)
    tg_user_id = mongoengine.IntField(required=True)
    tg_username = mongoengine.StringField()
    tg_first_name = mongoengine.StringField()
    tg_last_name = mongoengine.StringField()
    current_score = mongoengine.IntField(required=True, default=0)

    def change_score(self, score_delta, issuer, message):
        # everything here should be one transaction,
        # however MongoEngine doesn't allow that for now
        transaction = ProfileTransaction(
            chat_user_profile=self,
            score_delta=score_delta,
            issuer=issuer,
            message=message,
        )
        transaction.save()
        self.modify(inc__current_score=score_delta)

    @property
    def profile_transactions(self):
        return ProfileTransaction.objects(chat_user_profile=self)

    @property
    def tg_full_name(self):
        return f'{self.tg_first_name} {self.tg_last_name}'

class ProfileTransaction(mongoengine.Document):
    chat_user_profile = mongoengine.ReferenceField(ChatUserProfile)
    score_delta = mongoengine.IntField(required=True)
    issuer = mongoengine.ReferenceField(ChatUserProfile, required=True)
    message = mongoengine.DictField()
    date = mongoengine.IntField()
