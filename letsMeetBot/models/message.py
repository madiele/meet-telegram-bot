from django.db import models
from letsMeetBot.models import User, Chat
import telegram
import logging

logger = logging.getLogger("bot")


class Message(models.Model):
    message_id = models.IntegerField()
    from_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    from_chat = models.ForeignKey(
        Chat, on_delete=models.SET_NULL, blank=True, null=True
    )
    date = models.DateTimeField()
    text = models.CharField(max_length=4096, blank=True, null=True)
    pinned_message = models.BooleanField(default=False)
    link = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def get_private_share_link(message_id, chat_id):
        clean_chat_id = (
            str(abs(chat_id) - 1000000000000)
            if chat_id < -1000000000000
            else str(abs(chat_id))
        )
        return "https://t.me/c/" + clean_chat_id + "/" + str(message_id)

    @staticmethod
    def get_hashtags(bot_message: telegram.Message):
        entities = bot_message.entities
        hashtags = []
        for entity in entities:  # type: telegram.MessageEntity
            if entity.type == entity.HASHTAG:
                start = entity.offset + 1
                end = entity.offset + entity.length
                hashtag = bot_message.text[start:end]
                hashtags.append(hashtag)

        return hashtags

    @staticmethod
    def import_message(bot_message: telegram.Message):
        message = Message()
        message.message_id = bot_message.message_id
        if bot_message.new_chat_members:
            message.from_user = User.get_user(bot_user=bot_message.new_chat_members[0])
            message.text = "!!!new member!!!"
        else:
            message.from_user = User.get_user(bot_user=bot_message.from_user)
            message.text = "user chat message"
        message.from_chat = Chat.get_chat(bot_chat=bot_message.chat)
        message.date = bot_message.date
        message.pinned_message = True if bot_message.pinned_message else False
        message.link = bot_message.link
        message.save()
        return message
