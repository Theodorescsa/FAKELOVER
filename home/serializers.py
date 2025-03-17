from rest_framework import serializers
from .models import *

class ChatBotTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotType
        fields = "__all__"

class ChatAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatApp
        fields = "__all__"

class ChatBotTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotType
        fields = "__all__"

class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Hiển thị username thay vì ID
    chatbot = serializers.StringRelatedField()

    class Meta:
        model = Subscription
        fields = "__all__"

class BotSettingsSerializer(serializers.ModelSerializer):
    chatbot = serializers.StringRelatedField()  # Hiển thị tên chatbot

    class Meta:
        model = BotSettings
        fields = "__all__"

class SocialMediaAccountSerializer(serializers.ModelSerializer):
    chat_app = serializers.StringRelatedField()  # Hiển thị tên ứng dụng chat

    class Meta:
        model = SocialMediaAccount
        fields = "__all__"
