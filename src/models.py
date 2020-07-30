from mongoengine import Document, StringField, ReferenceField, IntField, BooleanField, DictField


class Chat(Document):
    tg_chat_id = IntField(required=True, primary_key=True)

    @property
    def profiles(self):
        return ChatUserProfile.objects(chat=self)

class ChatUserProfile(Document):
    chat = ReferenceField(Chat, required=True)
    tg_user_id = IntField(required=True)
    tg_username = StringField()
    tg_first_name = StringField()
    tg_last_name = StringField()
    current_score = IntField(required=True, default=0)

    def change_score(self, score_delta, issuer, message):
        self.current_score = self.current_score + score_delta
        transaction = ProfileTransaction(
            chat_user_profile=self,
            score_delta=score_delta,
            issuer=issuer,
            message=message,
        )
        transaction.save()
        self.save()

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
