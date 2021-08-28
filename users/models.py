from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
# from books.models import Book

# User._meta.get_field('email')._unique = True

class UserManager(BaseUserManager):
  """Define a model manager for User model with no username field."""

  use_in_migrations = True

  def _create_user(self, email, password, **extra_fields):
    """Create and save a User with the given email and password."""
    if not email:
        raise ValueError('The given email must be set')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password=None, **extra_fields):
    """Create and save a regular User with the given email and password."""
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    """Create and save a SuperUser with the given email and password."""
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
        raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
        raise ValueError('Superuser must have is_superuser=True.')

    return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
  username = None
  email = models.EmailField(_('email address'), unique = True)
  image = models.ImageField(upload_to='images/', blank = True)
  persian_username = models.CharField(max_length = 50, unique = True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = UserManager()


class Verification(models.Model):
  user = models.ForeignKey(
    User,
    null=True,
    on_delete=models.CASCADE
  )
  code = models.CharField(max_length=5, null=True)


class Author(models.Model):
  name = models.CharField(max_length=30)
  rate = models.FloatField(default=0.0)
  book_numbers = models.IntegerField(default=0)

  def __str__(self):
    return self.name


class Translator(models.Model):
  name = models.CharField(max_length=30)
  rate = models.FloatField(default=0.0)
  book_numbers = models.IntegerField(default=0)

  def __str__(self):
    return self.name
  
  
class Relationship(models.Model):
  following = models.ForeignKey(
    User,
    related_name="following",
    on_delete=models.CASCADE
  )
  follower = models.ForeignKey(
    User,
    related_name="follower",
    on_delete=models.CASCADE
  )

