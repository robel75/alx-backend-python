from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User

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

class MessageSerializer(serializers.ModelSerializer):
    
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

        def validate_message_body(self, value):
            if not value.strip():
                raise serializers.ValidationError("Message body cannot be empty.")
            if len(value) > 500:
                raise serializers.ValidationError("Message body is too long (max 500 characters).")
            return value

class ConversationSerializer(serializers.ModelSerializer):
    
    participants_id = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation

        fields = [
            "conversation_id",
            "participants_id",
            "messages",
            "created_at",
            "participant_count"
        ]

        read_only_fields = ["conversation_id", "created_id"]

    def get_participant_count(self, obj):
        return obj.participants_id.count()

