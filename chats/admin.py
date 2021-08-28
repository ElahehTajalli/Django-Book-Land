from django.contrib import admin
from chats.models import Message


class MessageAdmin(admin.ModelAdmin):
  list_display = ('id', 'sender', 'receiver', 'text', 'created_at')

admin.site.register(Message, MessageAdmin)
