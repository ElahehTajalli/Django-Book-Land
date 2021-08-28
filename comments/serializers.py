
from rest_framework import serializers
# from django.contrib.auth.models import User
from comments.models import Comment
from users.models import User
from users.serializers import UserSerializer
from posts.serializers import PostSerializer


class CommentSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  post = PostSerializer()

  class Meta:
    model = Comment
    fields = '__all__'


class CreateCommentSerializer(serializers.ModelSerializer):

  class Meta:
    model = Comment
    fields = '__all__'

class UpdateCommentSerializer(serializers.ModelSerializer):

  class Meta:
    model = Comment
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