# Generated by Django 2.2.5 on 2019-10-05 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('letsMeetBot', '0002_chat_timer_to_deletion'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='automatic_pin_character',
            field=models.CharField(blank=True, default=None, max_length=1, null=True),
        ),
        migrations.CreateModel(
            name='ChatUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_do_automatic_pin', models.BooleanField(default=False)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letsMeetBot.Chat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letsMeetBot.User')),
            ],
        ),
    ]