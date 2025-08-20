from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status, filters
from rest_framework.exceptions import ValidationError
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsConversationParticipant
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by("-created_at")
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()
        return conversation

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = MessageFilter
    ordering_fields = ["sent_at"]
    search_fields = ["content"]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        return Message.objects.filter(conversation=conversation).order_by("sent_at")

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        if not conversation.participants.filter(id=self.request.user.id).exists():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN, 
            )

        serializer.save(sender=self.request.user, conversation=conversation)
