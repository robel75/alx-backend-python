from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.exceptions import ValidationError
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by("-created_at")
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()
        return conversation


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("sent_at")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise ValidationError("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)
