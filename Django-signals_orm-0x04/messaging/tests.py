from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class MessagingSignalTest(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="password123")
        self.bob = User.objects.create_user(username="bob", password="password123")

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.alice,
            receiver=self.bob,
            content="Hello Bob!"
        )

        notification = Notification.objects.filter(user=self.bob, message=message).first()
        self.assertIsNotNone(notification)
        self.assertFalse(notification.is_read)

