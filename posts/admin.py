from django.contrib import admin
from posts.models import Post


class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'critic', 'book', 'rate', 'text', 'created_at')

admin.site.register(Post, PostAdmin)
