from django.db import models

from home.models import ChatApp, ChatBotType
from django.contrib.auth.models import User
# Create your models here.
# 4. Đăng ký sử dụng chatbot
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatbot = models.ForeignKey(ChatBotType, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.chatbot.name} ({'Active' if self.is_active else 'Expired'})"

# 5. Phiên chat giữa người dùng và chatbot
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatbot = models.ForeignKey(ChatBotType, on_delete=models.CASCADE)
    chat_app = models.ForeignKey(ChatApp, on_delete=models.SET_NULL, null=True)  # Messenger, Zalo, Telegram,...
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

# 7. Cấu hình chatbot (cho phép AI thay đổi nội dung tin nhắn)
class BotSettings(models.Model):
    chatbot = models.OneToOneField(ChatBotType, on_delete=models.CASCADE)
    response_speed = models.FloatField(default=1.0)  # Tốc độ phản hồi (s)
    personality = models.CharField(max_length=50, choices=[("friendly", "Thân thiện"), ("romantic", "Lãng mạn"), ("serious", "Nghiêm túc")], default="friendly")
    joke_frequency = models.IntegerField(default=3, help_text="Sau bao nhiêu tin nhắn sẽ chèn 1 câu đùa?")

    def __str__(self):
        return f"Cài đặt của {self.chatbot.name}"
