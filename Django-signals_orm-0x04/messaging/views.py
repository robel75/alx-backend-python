from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Message


User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        user.delete()  # triggers signals and deletes the account
        messages.success(request, "Your account has been deleted.")
        return redirect("home")  # or login page, etc.
    return render(request, "messaging/confirm_delete.html")  # optional confirmation page


@login_required
def conversation_view(request):
    # Messages where user is sender
    messages_sender = Message.objects.filter(sender=request.user).select_related('sender', 'receiver').prefetch_related('replies')
    
    # Messages where user is receiver
    messages_receiver = Message.objects.filter(receiver=request.user).select_related('sender', 'receiver').prefetch_related('replies')
    
    # Combine querysets
    messages = messages_sender | messages_receiver

    # Recursive helper to get threaded messages
    def get_threaded_messages(message):
        return {
            "message": message,
            "replies": [get_threaded_messages(reply) for reply in Message.objects.filter(parent_message=message)]
        }

    # Build threaded messages
    threaded_messages = [get_threaded_messages(msg) for msg in messages if msg.parent_message is None]

    return render(request, 'messaging/conversation.html', {'threaded_messages': threaded_messages})



