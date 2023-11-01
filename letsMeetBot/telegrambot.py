# -*- coding: utf-8 -*-
# Example code for telegrambot.py module

from django.conf import settings
from django_telegrambot.apps import DjangoTelegramBot
from letsMeetBot.models import (
    Chat,
    User,
    DailyStat,
    Message,
    ChatUser,
    BotSettings,
    Proposal,
)
import telegram
from time import sleep
import csv
import logging
import threading

logger = logging.getLogger("bot")
lock = False  # lock for save_to_google()

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


# only call this function in a separate thread
def timed_delete_message(message, time):
    """delete a message after a time in seconds"""
    sleep(time)
    try:
        message.delete()
        logger.info("message expired and was deleted")
    except:
        return


def welcome(update, context):
    bot = context.bot

    logger.info("new member foud!")
    chat = Chat.objects.get(pk=update.message.chat_id)
    try:
        welcome_message = chat.welcome_message.replace(
            "{name}", update.message.new_chat_members[0].full_name
        )

        if chat.last_welcome_message_id:
            logger.info("deleting last welcome message")
            try:
                bot.delete_message(update.message.chat_id, chat.last_welcome_message_id)
            except:
                pass

        message_sent = bot.send_message(
            update.message.chat_id,
            text=welcome_message,
            parse_mode=telegram.ParseMode.HTML,
            disable_notification=True,
            disable_web_page_preview=True,
        )
        chat.last_welcome_message_id = message_sent.message_id
        chat.save()

        logger.info("importing new users")
        for bot_user in update.message.new_chat_members:
            User.import_user(bot_user)

        logger.info("adding user to chat dump")
        Message.import_message(update.message)

        if chat.timer_to_deletion:
            logger.info(
                "welcome message set for deletion after "
                + str(chat.timer_to_deletion)
                + " seconds"
            )
            threading.Thread(
                target=timed_delete_message, args=[message_sent, chat.timer_to_deletion]
            ).start()

        logger.info("deleting join message to prevent notification")
        bot.delete_message(update.message.chat_id, update.message.message_id)

    except Exception as e:
        logger.error("failed to print welcome message")
        logger.error(e)

    if chat.log_chat:
        logger.info("logging new member to log chat")
        log_chat = chat.log_chat
        log_message = """[{chat_title}]\nNew member!\n\nName: <a href="tg://user?id={user_id}">{full_name}</a> @{username}\n#new_member #u{user_id} #c{chat_id}""".format(
            chat_title=update.message.chat.title,
            full_name=update.message.new_chat_members[0].full_name,
            username=update.message.new_chat_members[0].username,
            user_id=update.message.new_chat_members[0].id,
            chat_id=abs(update.message.chat.id),
        )
        bot.send_message(
            log_chat.chat_id,
            text=log_message,
            parse_mode=telegram.ParseMode.HTML,
            disable_notification=True,
        )

    # update daily stats
    logger.info("updating daily stats")
    today_stat = DailyStat.get_today_stat(chat.chat_id, bot)
    today_stat.new_members_count = today_stat.new_members_count + 1
    today_stat.save()


def new_message(update: telegram.Update, context: telegram.ext.CallbackContext):
    bot = context.bot

    try:
        TELEGRAM_NOTIFICATIONS = 777000
        if update.effective_user.id == TELEGRAM_NOTIFICATIONS:
            return
    except:
        pass

    logger.info("new message recived")

    chat = Chat.get_chat(update=update)

    logger.info("check if chat is enabled")
    # check if chat is authorized
    if not chat.enabled and update.effective_chat.type != telegram.Chat.CHANNEL:
        logger.warn(
            "chat "
            + str(chat.chat_name)
            + " is not enabled, enable it in the admin page"
        )
        return

    # check if there is a new member
    if update.message and update.message.new_chat_members:
        welcome(update, context)
    elif update.message and update.message.text:
        bot_message = update.message  # type: telegram.Message
        # log the message
        if (
            update.message.chat.type == telegram.Chat.SUPERGROUP
            or update.message.chat.type == telegram.Chat.GROUP
        ):
            logger.info("logging message")
            Message.import_message(bot_message=bot_message)

            logger.info("updating stats")
            today_stat = DailyStat.get_today_stat(chat.chat_id, bot)
            today_stat.messages_count = today_stat.messages_count + 1
            today_stat.save()

            logger.info("updating user stats")
            usr = User.get_user(update=update)
            usr.message_count = usr.message_count + 1
            usr.save()

            if (
                ChatUser.get_chat_user(chat, usr).can_do_automatic_pin
                and update.message.text[: len(chat.automatic_pin_sequence)]
                == chat.automatic_pin_sequence
            ):
                logger.info("pin character found, pinnig message")
                bot.pin_chat_message(chat.chat_id, update.message.message_id)

            logger.info("checking for hashtags")

            hashtags = Message.get_hashtags(bot_message)
            if hashtags:
                logger.info("found the following hashtags: " + str(hashtags))
                for hashtag in hashtags:
                    if hashtag == chat.publish_to_channel_hashtag and chat.chat_channel:
                        proposal = Proposal.new_proposal(bot_message)
                    break


def error(update, context):
    logger.warn('Update "%s" caused error "%s"' % (update, context.error))


def main():
    logger.info("Loading handlers for telegram bot")

    # initializing settings
    logger.info("initializing settings")
    try:
        BotSettings.get_bot_settings()
    except:
        pass

    dp = DjangoTelegramBot.dispatcher  # type: telegram.ext.Dispatcher
    dp.use_context = True
    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.all, new_message))
    dp.add_handler(
        telegram.ext.CallbackQueryHandler(Proposal.update_proposal_callback), group=1
    )
    # log all errors
    dp.add_error_handler(error)

    # checks if there is a csv in the IMPORTED_USERS heroku variable and import users if thats tha case
    if settings.IMPORTED_USERS:
        logger.info("users csv found, importing users")
        users_csv = settings.IMPORTED_USERS.splitlines()
        rd = csv.reader(users_csv, delimiter="\t")
        next(rd)  # skip the header line
        for row in rd:
            user = User()
            user.user_id = row[0]
            user.full_name = row[1]
            if row[2] != "—":
                user.username = row[2]
            user.message_count = int(row[3])
            user.save()
        logger.info("users imported")

    logger.info("done starting up")
