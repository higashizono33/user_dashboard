from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Message(models.Model):
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    to_whom = models.ForeignKey(User, related_name='receives', on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_recent(self):
        diff = timezone.now() - self.created_at
        return diff.seconds < 1800 #30mins ago

class Comment(models.Model):
    message = models.ForeignKey(Message, related_name='comments_to', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments_by', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def is_recent(self):
        diff = timezone.now() - self.created_at
        return diff.seconds < 1800 #30mins ago