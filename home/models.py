from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.db import models
from django.contrib.auth.models import User

# 1. Ứng dụng nhắn tin (Messenger, Zalo, Telegram, v.v.)
class ChatApp(models.Model):
    name = models.CharField(max_length=100, verbose_name="App Name")
    icon = models.ImageField(upload_to="chat_apps/", null=True, blank=True)  # Icon của app

    def __str__(self):
        return self.name

# 2. Loại ChatBot (Bố, Mẹ, Người yêu, Bạn thân, v.v.)
class ChatBotType(models.Model):
    name = models.CharField(max_length=100, verbose_name="ChatBot Name")
    description = models.TextField(null=True, blank=True)  # Mô tả chatbot
    price = models.FloatField(default=0.0)  # Giá thuê chatbot
    voice_tone = models.CharField(max_length=50, choices=[("warm", "Ấm áp"), ("funny", "Hài hước"), ("cold", "Lạnh lùng")], default="warm")  # Giọng điệu AI

    def __str__(self):
        return f"{self.name} - {self.price}"

# 3. Hồ sơ người dùng
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chat_apps = models.ManyToManyField(ChatApp, blank=True, related_name="userprofile")  # Người dùng chọn app nào để kết nối chatbot
    balance = models.FloatField(default=0.0)  # Số dư tài khoản
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# 4. Đăng ký sử dụng chatbot
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatbot = models.ForeignKey(ChatBotType, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.chatbot.name} ({'Active' if self.is_active else 'Expired'})"

# 7. Cấu hình chatbot (cho phép AI thay đổi nội dung tin nhắn)
class BotSettings(models.Model):
    chatbot = models.OneToOneField(ChatBotType, on_delete=models.CASCADE)
    response_speed = models.FloatField(default=1.0)  # Tốc độ phản hồi (s)
    personality = models.CharField(max_length=50, choices=[("friendly", "Thân thiện"), ("romantic", "Lãng mạn"), ("serious", "Nghiêm túc")], default="friendly")
    joke_frequency = models.IntegerField(default=3, help_text="Sau bao nhiêu tin nhắn sẽ chèn 1 câu đùa?")

    def __str__(self):
        return f"Cài đặt của {self.chatbot.name}"

class SocialMediaAccount(models.Model):
    chat_app = models.ForeignKey(ChatApp,on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    app_pass = models.CharField(max_length=100)
    is_activate = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.username}-{self.chat_app.name}"