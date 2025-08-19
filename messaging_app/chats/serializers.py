from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user

        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]
        
        read_only_fields = ["user_id","created_at"]

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation

        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]

        read_only_fields = ["conversation_id", "created_id"]

class MessageSerializer(serializers.ModelSerializers):
    
    sender = UserSerializer(read_only = True)

    class Meta:
        model = Message

        fields = [
            "message_id",
            "conversation",
            "sender",
            "message_body",
            "sent_at",
        ]

        read_only_fields = ["conversation_id", "created_at"]