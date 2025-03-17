# Generated by Django 4.2.20 on 2025-03-17 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatsession',
            name='chat_app',
        ),
        migrations.RemoveField(
            model_name='chatsession',
            name='chatbot',
        ),
        migrations.RemoveField(
            model_name='chatsession',
            name='user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='session',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='chatbot',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='user',
        ),
        migrations.DeleteModel(
            name='BotSettings',
        ),
        migrations.DeleteModel(
            name='ChatSession',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
