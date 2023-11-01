from django.db import models
from django.contrib.postgres.fields import ArrayField
import telegram
from letsMeetBot.models import Message, Chat, User, ChatUser
from typing import Union

import logging
logger = logging.getLogger('bot')

class Proposal(models.Model):
    from_message_id = models.IntegerField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    proposed_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    voted_by_ids = ArrayField(models.IntegerField(), default=list)
    proposal_id = models.IntegerField(primary_key=True)
    shared_to_channel = models.BooleanField(default=False)

    def add_like(self, user_id):
        logger.info("user: " + str(user_id) + " liked")
        self.voted_by_ids.append(user_id)
        self.save()

    def remove_like(self, user_id):
        logger.info("user: " + str(user_id) + " removed the like")
        self.voted_by_ids.remove(user_id)
        self.save()
            
    def get_keyboard(self):
        logger.info("generating keyboard")
        likes = self.get_likes()
        keyboard = telegram.InlineKeyboardMarkup.from_button(telegram.InlineKeyboardButton(str(likes) + " 👍", callback_data=str(likes)))
        logger.info("keyboard generated")
        return keyboard

    def get_likes(self):
        return len(self.voted_by_ids)

    def share_to_channel(self, bot: telegram.Bot):
        bot.forward_message(chat_id=self.chat.chat_channel.chat_id, from_chat_id=self.chat.chat_id, message_id=self.from_message_id)
        bot.send_message(chat_id=self.chat.chat_channel.chat_id, text="link to the message: "+Message.get_private_share_link(self.from_message_id, self.chat.chat_id))
        self.shared_to_channel = True
        self.save()

    def update_proposal_callback(update: telegram.Update, context: telegram.ext.CallbackContext):
        logger.info("updating proposal")
        callback_query = update.callback_query #type: telegram.CallbackQuery
        proposal = Proposal.get_proposal(callback_query.message)
        user_id = callback_query.from_user.id
        chat_user = ChatUser.get_chat_user(proposal.chat, User.get_user(bot_user=callback_query.from_user))

        if user_id not in proposal.voted_by_ids:
            proposal.add_like(user_id)
            callback_query.bot.answer_callback_query(callback_query.id, "👍 added")
        else:
            proposal.remove_like(user_id)
            callback_query.bot.answer_callback_query(callback_query.id, "👍 removed")

        if (chat_user.instant_share_to_channel or proposal.get_likes() >= proposal.chat.proposal_to_channel_threshold) and not proposal.shared_to_channel:
            proposal.share_to_channel(callback_query.bot)

        text = proposal.chat.proposal_message
        context.bot.edit_message_text(text, chat_id=proposal.chat.chat_id, message_id=proposal.proposal_id, reply_markup=proposal.get_keyboard(), disable_web_page_preview=True)


    @staticmethod
    def new_proposal(message: telegram.Message) -> 'Proposal':
        logger.info("adding new proposal")
        proposal = Proposal()
        proposal.from_message_id = message.message_id
        proposal.proposed_by = User.get_user(bot_user=message.from_user)
        proposal.chat = Chat.get_chat(bot_chat=message.chat)
        proposal.voted_by_ids.append(proposal.proposed_by.user_id)
        proposal.proposal_id = message.reply_text(proposal.chat.proposal_message, reply_markup=proposal.get_keyboard(), disable_web_page_preview=True).message_id
        proposal.save()
        return proposal

    @staticmethod
    def get_proposal(data: Union[telegram.Message, Message]) -> 'Proposal':
        message_id = data.message_id
        logger.info("retriving proposal with id: " + str(message_id))
        return Proposal.objects.get(pk=message_id)

