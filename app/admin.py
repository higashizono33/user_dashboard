from django.contrib import admin
from .models import Message, Comment

class MessageAdmin(admin.ModelAdmin):
    pass
class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Message, MessageAdmin)
admin.site.register(Comment, CommentAdmin)
