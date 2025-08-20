from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsConversationParticipant(BasePermission):

    def has_object_permission(self, request, view, obj):
        # obj could be Conversation or Message
        if hasattr(obj, "participants"):  # Conversation
            return obj.participants.filter(id=request.user.id).exists()
        if hasattr(obj, "conversation"):  # Message
            return obj.conversation.participants.filter(id=request.user.id).exists()
        return False
