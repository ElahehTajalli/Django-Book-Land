from django.db import models
from users.models import User
from books.models import Book

class Post(models.Model):
  critic = models.ForeignKey(
    User,
    on_delete=models.CASCADE
  )
  book = models.ForeignKey(
    Book,
    on_delete=models.CASCADE
  )
  rate = models.FloatField()
  likes = models.ManyToManyField(User, related_name="likes", blank=True)
  dislikes = models.ManyToManyField(User, related_name="dislikes", blank=True)
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)