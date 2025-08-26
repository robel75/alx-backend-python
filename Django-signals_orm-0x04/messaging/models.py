from django.db import models
import uuid
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Message(models.Model):
    message_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    sender = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "sent_messages"
    )
    receiver = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "recieved_messages"
    )
    content = models.TextField()
    timestamp= models.DateTimeField(auto_now_add=True)

    def __str__(self)->str:
        return f"message from {self.sender} to {self.reciever} at {self.timestamp}"

class Notification(models.Model):
    notification_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "notifications"
    )
    message = models.ForeignKey(
        Message,
        on_delete= models.CASCADE,
        related_name= "notifications"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self)-> str:
        return f"Notification for {self.user}- msg {self.message_id}"
