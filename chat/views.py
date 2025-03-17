from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import ChatSession
from .serializers import ChatSessionSerializer
# Create your views here.
def chat_page(request):
    return render(request,'chat/chat_page.html')



class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
