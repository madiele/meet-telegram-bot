from django.db import models
import logging
logger = logging.getLogger('bot')


class Chat(models.Model):
    chat_id = models.BigIntegerField(primary_key=True)
    chat_name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    log_chat = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    chat_channel = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='chat_channels')
    welcome_message = models.TextField(blank=True, null=True)
    last_welcome_message_id = models.IntegerField(null=True, blank=True)
    timer_to_deletion = models.IntegerField(default=0)
    automatic_pin_sequence = models.CharField(max_length=255, default=None, blank=True, null=True)
    publish_to_channel_hashtag = models.CharField(max_length=255, default=None, blank=True, null=True)
    proposal_message = models.TextField(max_length=1024, default="do you like the proposal?")
    proposal_to_channel_threshold = models.IntegerField(default=5)

    @staticmethod
    def get_chat(update=None, bot_chat=None, chat_id=None, bot=None):
        if update:
            try:
                logger.info("looking for chat in database")
                return Chat.objects.get(chat_id__exact=update.effective_chat.id)
            except Chat.DoesNotExist: # if chat does not exist add it to the known chats
                logger.info("new chat recognized, enable it in the admin page")
                bot_chat = update.effective_chat
                bot_chat.send_message(text="to enable this bot be sure to authorize the chat in the admin page", disable_notification=True)
                chat = Chat.import_chat(bot_chat)
                return chat
        elif chat_id and bot:
            try:
                logger.info("looking for chat in database")
                return Chat.objects.get(chat_id__exact=chat_id)
            except Chat.DoesNotExist: # if chat does not exist add it to the known chats
                logger.info("new chat recognized, enable it in the admin page")
                bot_chat = bot.get_chat(chat_id)
                bot_chat.send_message(text="to enable this bot be sure to authorize the chat in the admin page", disable_notification=True)
                chat = Chat.import_chat(bot_chat)
                return chat
        elif bot_chat:
            try:
                return Chat.objects.get(chat_id__exact=bot_chat.id)
            except Chat.DoesNotExist:
                chat = Chat.import_chat(bot_chat)
                return chat
        else:
            raise ValueError("this function requirese either an update or both chat_id and telegramtelegram.bot or a telegram.chat")

    @staticmethod
    def import_chat(bot_chat):
        chat = Chat()
        chat.chat_id = bot_chat.id
        chat.chat_name = bot_chat.first_name if bot_chat.type == "private" else bot_chat.title
        chat.enabled = False
        chat.save()
        return chat


    def __str__(self):
        return self.chat_name
