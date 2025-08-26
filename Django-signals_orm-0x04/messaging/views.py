from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        user.delete()  # triggers signals and deletes the account
        messages.success(request, "Your account has been deleted.")
        return redirect("home")  # or login page, etc.
    return render(request, "messaging/confirm_delete.html")  # optional confirmation page

def get_threaded_messages(message):
    return {
        "message": message,
        "replies": [get_threaded_messages(reply) for reply in message.replies.all()]
    }


