from django.db import models
import logging
logger = logging.getLogger('bot')

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    is_bot = models.BooleanField(default=False)
    full_name = models.CharField(max_length=510,blank=True, null=True)
    username = models.CharField(max_length=255,blank=True, null=True)
    message_count = models.IntegerField(default=0)
    warns = models.IntegerField(default=0)

    @staticmethod
    def get_user(update=None, bot_user=None):
        if update:
            try:
                return User.objects.get(pk=update.effective_user.id)
            except User.DoesNotExist:
                up_user = update.effective_user
                new_user = User.import_user(up_user)
                return new_user
        elif bot_user:
            try:
                return User.objects.get(pk=bot_user.id)
            except User.DoesNotExist:
                new_user = User.import_user(bot_user)
                return new_user
        else:
            raise ValueError("get_user requires either telegra.update or telegram.user")

    @staticmethod
    def import_user(bot_user):
        user = User()
        user.user_id = bot_user.id
        user.is_bot = bot_user.is_bot
        user.full_name = bot_user.full_name
        user.username = bot_user.username
        user.save()
        return user

    class meta:
       verbose_name = 'User'
       verbose_name_plural = 'Users'

    def __str__(self):
        return self.full_name + (" ("+self.username+")" if self.username else "")
