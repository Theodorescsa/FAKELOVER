from django.urls import path
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatBotTypeViewSet

app_name = "home"
router = DefaultRouter()
router.register(r'chat-apps', ChatAppViewSet)
router.register(r'chatbots', ChatBotTypeViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'bot-settings', BotSettingsViewSet)
router.register(r'social-accounts', SocialMediaAccountViewSet)
urlpatterns = [
    path("api/", include(router.urls)),
    path('', home_page, name='home-page'),
    path('login-page/', login_page, name='login-page'),
    path('chatbots-page', chatbots_page, name='chatbots-page'),
    path("api/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/logout/", logout_view, name="logout"),
]

