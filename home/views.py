from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import *
from .serializers import *
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view

# View đăng nhập để trả JWT trong cookies
class CustomTokenObtainPairView(TokenObtainPairView):
    @extend_schema(tags=["app_home"])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]

        # Đặt Access Token trong HTTP-Only Cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=False,
            secure=True,  # Chỉ bật nếu chạy HTTPS
            samesite="Lax",
            path="/"
        )

        # Đặt Refresh Token trong Cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=False,
            secure=True,
            samesite="Lax",
            path="/"
        )

        return response

# API Đăng xuất: Xóa cookie chứa token
@extend_schema(tags=["app_home"])
def logout_view(request):
    logout(request)
    return redirect("home:home-page")

def login_page(request):
    return render(request,"home/login_page.html")
    
# Create your views here.
def home_page(request):
    return render(request,'home/home_page.html')

def chatbots_page(request):
    return render(request,'home/chatbot_page.html')

@extend_schema(tags=["app_home"])
class ChatBotTypeViewSet(viewsets.ModelViewSet):
    queryset = ChatBotType.objects.all()
    serializer_class = ChatBotTypeSerializer
    permission_classes = [IsAuthenticated]
@extend_schema(tags=["app_home"])
class ChatAppViewSet(viewsets.ModelViewSet):
    queryset = ChatApp.objects.all()
    serializer_class = ChatAppSerializer
    permission_classes = [IsAuthenticated]
@extend_schema(tags=["app_home"])
class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
@extend_schema(tags=["app_home"])
class BotSettingsViewSet(viewsets.ModelViewSet):
    queryset = BotSettings.objects.all()
    serializer_class = BotSettingsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
@extend_schema(tags=["app_home"])
class SocialMediaAccountViewSet(viewsets.ModelViewSet):
    queryset = SocialMediaAccount.objects.all()
    serializer_class = SocialMediaAccountSerializer
    permission_classes = [IsAuthenticated]
