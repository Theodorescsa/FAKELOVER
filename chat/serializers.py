from rest_framework import serializers
from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import ChatSession, ChatBotType, SocialMediaAccount
from home.models import ChatApp, Subscription, BotSettings
from rest_framework.response import Response

class BotSettingsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotSettings
        fields = ["response_speed", "personality", "joke_frequency"]
class SocialMediaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaAccount
        fields = ["id", "chat_app", "username"]  # Chọn các trường có thể serialize

class ChatSessionGetSerializer(serializers.ModelSerializer):
    social_account = SocialMediaAccountSerializer()  # Dùng serializer để tránh lỗi

    class Meta:
        model = ChatSession
        fields = '__all__'

class ChatSessionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    bot_settings = BotSettingsPostSerializer(required=False)
    social_account = SocialMediaAccountSerializer(required=False)  # Chấp nhận ID hoặc object mới

    class Meta:
        model = ChatSession
        fields = ["id", "user", "chatbot", "social_account", "started_at", "bot_settings"]

    def create(self, validated_data):
        user = validated_data.get("user")
        chatbot = validated_data.get("chatbot")
        request = self.context["request"]
        social_account_data = request.data.get("social_account", None)
        social_account_data_pop = validated_data.pop("social_account", None)

        bot_settings_data = validated_data.pop("bot_settings", None)
        print(social_account_data)
        # Nếu social_account_data là số (ID), lấy tài khoản có sẵn
        if isinstance(social_account_data, int):
            social_account = SocialMediaAccount.objects.get(id=social_account_data)
        elif isinstance(social_account_data, dict):  
            print(social_account_data.get("chat_app"))
            print(social_account_data.get("password"))
            # Nếu là object, tạo mới SocialMediaAccount
            chatapp = ChatApp.objects.get(id=int(social_account_data.get("chat_app")))
            social_account = SocialMediaAccount.objects.create(
                chat_app=chatapp,
                username=social_account_data.get("username"),
                app_pass=social_account_data.get("password")
            )
        else:
            social_account = None

        # Xử lý BotSettings (nếu có)
        bot_settings, created = BotSettings.objects.get_or_create(
            chatbot=chatbot,
            defaults={
                "response_speed": bot_settings_data.get("response_speed", 1.0),
                "personality": bot_settings_data.get("personality", "friendly"),
                "joke_frequency": bot_settings_data.get("joke_frequency", 3),
            }
        )
        if not created and bot_settings_data:
            for attr, value in bot_settings_data.items():
                setattr(bot_settings, attr, value)
            bot_settings.save()

        # Tạo Subscription nếu có social_account
        if social_account:
            Subscription.objects.get_or_create(
                user=user,
                chatbot=chatbot,
                defaults={"end_date": now().replace(year=now().year + 1), "is_active": True}
            )

        chat_session = ChatSession.objects.create(**validated_data)
        return chat_session
