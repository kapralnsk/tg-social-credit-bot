from mongoengine import Document, StringField, ReferenceField, IntField, BooleanField, DictField


class Chat(Document):
    tg_chat_id = IntField(required=True, primary_key=True)

    def get_profiles(self, order_by=tuple()):
        profiles = ChatUserProfile.objects(chat=self).order_by(*order_by)
        return profiles

class ChatUserProfile(Document):
    chat = ReferenceField(Chat, required=True)
    tg_user_id = IntField(required=True)
    tg_username = StringField()
    tg_first_name = StringField()
    tg_last_name = StringField()
    current_score = IntField(required=True, default=0)

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

class ProfileTransaction(Document):
    chat_user_profile = ReferenceField(ChatUserProfile)
    score_delta = IntField(required=True)
    issuer = ReferenceField(ChatUserProfile, required=True)
    message = DictField()
    date = IntField()
