from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsConversationParticipant(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        # Check for Conversation
        if hasattr(obj, "participants"):
            return obj.participants.filter(id=request.user.id).exists()

        # Check for Message
        if hasattr(obj, "conversation"):
            is_participant = obj.conversation.participants.filter(id=request.user.id).exists()

            if not is_participant:
                return False

            if request.method in ["PUT", "PATCH", "DELETE"]:
                return True  

            # Allow participants to view messages
            if request.method in SAFE_METHODS:
                return True  

        return False
