# Generated by Django 2.2.5 on 2019-10-03 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letsMeetBot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='timer_to_deletion',
            field=models.IntegerField(default=0),
        ),
    ]
