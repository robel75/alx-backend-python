from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.core.exceptions import ValidationError

class Roles(models.TextChoices):
    GUEST = 'Guest', 'guest'
    HOST = 'Host', 'host'
    ADMIN = 'Admin', 'admin'


class User(AbstractUser):
    user_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )

    email = models.EmailField(unique = True)
    created_at = models.DateTimeField(auto_now_add = True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=32, null=True, blank=True)

    role = models.CharField(
        max_length = 10,
        choices = Roles.choices,
        default = Roles.GUEST
    )

    groups = models.ManyToManyField(
        Group,
        related_name='chats_users',  #  change to unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='chats_users_permissions',  #  unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


    class Meta:
        indexes = [
            models.Index(fields=["role"]),
        ]
    
    def __str__(self) -> str:
        return f"{self.username} ({self.email})"

class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )

    participants_id = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name = "conversations",
        help_text = "users taking part in this conversation"
    )
    
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        names = list(self.participants.values_list("username", flat=True)[:2])
        more = self.participants.count() - len(names)
        end = f" +{more}" if more > 0 else ""
        return f"Conversation({', '.join(names)}{end})"


class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sent_at"]
        indexes = [
            models.Index(fields=["conversation", "sent_at"]),
            models.Index(fields=["sender", "sent_at"]),
        ]

    def __str__(self) -> str:
        return f"Msg from {self.sender} at {self.sent_at:%Y-%m-%d %H:%M}"

    def clean(self):
        if self.pk is None and self.sender_id and self.conversation_id:
            if not self.conversation.participants.filter(pk=self.sender_id).exists():
                raise ValidationError("Sender must be a participant in the conversation.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
