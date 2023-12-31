# Generated by Django 2.2.5 on 2019-10-07 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('letsMeetBot', '0005_botsettings_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='chat_channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_channels', to='letsMeetBot.Chat'),
        ),
        migrations.AddField(
            model_name='chat',
            name='publish_to_channel_hashtag',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='chatuser',
            name='can_share_to_channel',
            field=models.BooleanField(default=False),
        ),
    ]
