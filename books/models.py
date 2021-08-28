from django.db import models
from users.models import Author, Translator, User

class Book(models.Model):
  name = models.CharField(max_length=50)
  author = models.ForeignKey(
    Author,
    on_delete=models.CASCADE
  )
  publisher = models.CharField(max_length=30)
  genre = models.CharField(max_length=30)
  rate = models.FloatField(default=0.0)
  rate_numbers = models.IntegerField(default=0)
  publication_year = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  translator = models.ForeignKey(
    Translator,
    null=True,
    on_delete=models.CASCADE
  )
  image = models.ImageField(upload_to='images/')
  summary = models.TextField(null=True)


class Rate(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
  )
  book = models.ForeignKey(
    Book,
    related_name="book_rate",
    on_delete=models.CASCADE
  )
  rate = models.FloatField(default=0.0)


class Plan(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
  )
  wants_to_read = models.ManyToManyField(Book, related_name="wants_to_read", blank=True)
  read = models.ManyToManyField(Book, related_name="read", blank=True)
  reading = models.ManyToManyField(Book, related_name="reading", blank=True)
  
  
class Favorite(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
  )
  book = models.ForeignKey(
    Book,
    on_delete=models.CASCADE
  )
  created_at = models.DateTimeField(auto_now_add=True)