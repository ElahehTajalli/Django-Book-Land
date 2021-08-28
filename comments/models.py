from django.db import models
from users.models import User
from posts.models import Post

class Comment(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
  )
  post = models.ForeignKey(
    Post,
    on_delete=models.CASCADE
  )
  likes = models.ManyToManyField(User, related_name="comment_likes", blank=True)
  dislikes = models.ManyToManyField(User, related_name="comment_dislikes", blank=True)
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)