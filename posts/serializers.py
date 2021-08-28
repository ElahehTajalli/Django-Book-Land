
from rest_framework import serializers
# from django.contrib.auth.models import User
from posts.models import Post
from users.models import User
from users.serializers import UserSerializer
from books.serializers import BookSerializer


class PostSerializer(serializers.ModelSerializer):
  critic = UserSerializer()
  book = BookSerializer()

  class Meta:
    model = Post
    fields = '__all__'


class CreatePostSerializer(serializers.ModelSerializer):

  class Meta:
    model = Post
    fields = '__all__'


class UpdatePostSerializer(serializers.ModelSerializer):

  class Meta:
    model = Post
    fields = '__all__'

  def update(self, instance, validated_data):
    user = User.objects.get(
      id = self.context['user']
    )
    if self.context['action'] == 'like':
      instance.likes.add(user)
    if self.context['action'] == 'dislike':
      instance.dislikes.add(user)

    instance.save()
    return instance
