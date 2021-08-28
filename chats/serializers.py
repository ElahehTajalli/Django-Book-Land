
from rest_framework import serializers
from users.models import User
from chats.models import Message
from users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
  receiver = UserSerializer()
  sender = UserSerializer()

  class Meta:
    model = Message
    fields = '__all__'


class CreateMessageSerializer(serializers.ModelSerializer):

  class Meta:
    model = Message
    fields = '__all__'