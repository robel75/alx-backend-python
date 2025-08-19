from django.db import models

# Create your models here.
class user(Abstractuser):
    profile_picture = models.ImageField(
        upload_to = 'profile_pics/',
        Null=True, blank=True
        )
    
    date_of_birth = models.DateField(
        blank = True,
        Null = True
        )
    last_seen = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)

    class meta:
        verbose_name = "User"
        verbose_name_plural = "users"
    
    def __str__(self):
        return self.username

class conversation(models.Model):
    is_group_chat = models.BooleanField(
        default=False, 
        verbose_name="Group Chat")
    class meta:
        verbose_name = "conversation"
        verbose_name_plural = "conversations"
    
    def __str__(self):
        return self.username

class message(models.Model):
    
