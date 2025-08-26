from django.contrib import admin
from .models import Message, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "sender", "reciever", "content", "timestamp")
    search_fields = ("sender__username", "receiver__username", "content")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("notification_id", "user", "message", "created_at", "is_read")
    list_filter = ("is_read",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "sender", "receiver", "parent_message", "timestamp")


