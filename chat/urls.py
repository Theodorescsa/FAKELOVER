from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatSessionViewSet, chat_page

router = DefaultRouter()
router.register(r'chatsessions', ChatSessionViewSet)

urlpatterns = [
    path('', chat_page, name='chat-page'),
    path('api/', include(router.urls)),
    
]
