from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions

class IsConversationParticipant(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
        return False
        if hasattr(obj, "participants"):  # Conversation
            return obj.participants.filter(id=request.user.id).exists()
        if hasattr(obj, "conversation"):  # Message
            return obj.conversation.participants.filter(id=request.user.id).exists()
        return False
