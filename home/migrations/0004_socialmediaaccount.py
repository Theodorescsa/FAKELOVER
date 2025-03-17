# Generated by Django 4.2.20 on 2025-03-17 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_subscription_botsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('is_activate', models.BooleanField(default=False)),
                ('chat_app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.chatapp')),
            ],
        ),
    ]
