from django.db import models
from letsMeetBot.models import Chat, User
import logging
logger = logging.getLogger('bot')

class ChatUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    can_do_automatic_pin = models.BooleanField(default=False)
    instant_share_to_channel = models.BooleanField(default=False)

    @staticmethod
    def get_chat_user(chat: Chat, user: User) -> 'ChatUser':
        try:
            return ChatUser.objects.get(user__user_id__exact=user.user_id, chat__chat_id__exact=chat.chat_id)
        except ChatUser.DoesNotExist:
            return ChatUser.import_chat_user(chat, user)


    @staticmethod
    def import_chat_user(chat: Chat, user: User) -> 'ChatUser':
        chat_user = ChatUser()
        chat_user.chat = chat
        chat_user.user = user
        chat_user.save()
        return chat_user

    def __str__(self):
        return str(self.user) + " of " + str(self.chat)
