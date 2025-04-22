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
from django.contrib import messages
from .forms import LoginForm
# API Đăng xuất: Xóa cookie chứa token
@extend_schema(tags=["app_home"])
def logout_view(request):
    logout(request)
    return redirect("home:home-page")

def login_page(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                context = {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'username': user.username
                }
                return render(request, "home/chatbot_page.html", context)
            else:
                form.add_error(None, "Sai tài khoản hoặc mật khẩu")

    return render(request, "home/login_page.html", {'form': form})
# Create your views here.
def home_page(request):
    return render(request,'home/home_page.html')

def chatbots_page(request):
    
    if request.user.is_authenticated:
        refresh = RefreshToken.for_user(request.user)
        context = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        print('context',context)
    else:
        context = {
            'access_token': '',
            'refresh_token': '',
        }

    return render(request, 'home/chatbot_page.html', context)
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
