from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, cretaed, **kwargs):
    if created:
        Notification.objects.create(
            user = instance.reciever,
            message=instance
        )

from django.db.models.signals import pre_save
from .models import MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Only act if this is an existing message being updated
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        # If content changed, save old content
        if old_message.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            instance.edited = True  # mark as edited
