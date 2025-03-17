from django.contrib import admin
from .models import ChatApp, ChatBotType, SocialMediaAccount, UserProfile, Subscription, BotSettings

@admin.register(ChatApp)
class ChatAppAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "icon")

@admin.register(ChatBotType)
class ChatBotTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "voice_tone")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance", "created_at")

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "chatbot", "start_date", "end_date", "is_active")

@admin.register(BotSettings)
class BotSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "chatbot", "response_speed", "personality", "joke_frequency")

@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_app", "username", "app_pass", "is_activate")
