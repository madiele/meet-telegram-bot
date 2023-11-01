from django.db import models
from datetime import date
from letsMeetBot.models import Chat

class DailyStat(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.SET_NULL, null=True)
    members_count = models.IntegerField(null=True, blank=True)
    new_members_count = models.IntegerField(default=0)
    messages_count = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)

    class meta:
        constraints = [
                    models.UniqueConstraint(fields=['chat', 'date'], name='unique_stat') 
                ]

    @staticmethod
    def get_today_stat(chat_id, bot):
        try:
            today_stat = DailyStat.objects.get(date__exact=date.today(), chat__chat_id__exact=chat_id)
            today_stat.members_count = bot.get_chat_members_count(chat_id)
            return today_stat
        except DailyStat.DoesNotExist:
            today_stat = DailyStat()
            today_stat.chat = Chat.objects.get(chat_id__exact=chat_id)
            today_stat.members_count = bot.get_chat_members_count(chat_id)
            today_stat.new_members_count = 0
            return today_stat
