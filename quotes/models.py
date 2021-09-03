from django.db import models
from users.models import User
from books.models import Book

class Quote(models.Model):
  author = models.CharField(max_length=50)
  book = models.CharField(max_length=50, null=True, blank = True)
  text = models.TextField()
  image = models.ImageField(upload_to='images/')
  likes = models.ManyToManyField(User, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)