
from rest_framework import serializers
# from django.contrib.auth.models import User
from quotes.models import Quote
from users.models import User
from users.serializers import UserSerializer
from posts.serializers import PostSerializer


class QuoteSerializer(serializers.ModelSerializer):

  class Meta:
    model = Quote
    fields = '__all__'

class UpdateQuoteSerializer(serializers.ModelSerializer):

  class Meta:
    model = Quote
    fields = '__all__'

  def update(self, instance, validated_data):
    user = User.objects.get(
      id = self.context['user']
    )
    instance.likes.add(user)
    instance.save()
    return instance