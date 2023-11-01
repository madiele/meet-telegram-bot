from django.db import models
from django.utils.translation import ugettext_lazy as _
from timezone_field import TimeZoneField

class BotSettings(models.Model):
    instance = models.CharField(max_length=20, default="instance", primary_key=True)
    timezone = TimeZoneField(default='Europe/Rome')

    @staticmethod
    def get_bot_settings():
        try:
            return BotSettings.objects.get(instance__exact="instance")
        except BotSettings.DoesNotExist:
            settings = BotSettings()
            settings.save()
            return settings


    def __str__(self):
        return 'settings'

    class meta:
        verbose_name = _('Bot Settings')
        verbose_name_plural = _('Bot Settings')


