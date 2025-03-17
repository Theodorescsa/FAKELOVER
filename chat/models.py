from django.db import models

from home.models import ChatApp, ChatBotType, SocialMediaAccount
from django.contrib.auth.models import User
# Create your models here.

# 5. Phiên chat giữa người dùng và chatbot
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatbot = models.ForeignKey(ChatBotType, on_delete=models.CASCADE)
    social_account = models.ForeignKey(SocialMediaAccount, on_delete=models.SET_NULL, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.user.username} với {self.chatbot.name} trên {self.chat_app.name}"

# 6. Tin nhắn trong phiên chat
class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=[("user", "User"), ("bot", "Chatbot")])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.sender}: {self.content[:50]}"

