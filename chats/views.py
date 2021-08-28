
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from django.shortcuts import render
from chats.serializers import *
from chats.models import *
from users.serializers import *
from users.models import *
from django.db.models import Q

class messageView (APIView):

  def post(self, request):
    data = {
      'sender': request.user.id,
      'receiver': request.POST['receiver'],
      'text': request.POST['text']
    }
    message = CreateMessageSerializer(
      data = data
    )

    if message.is_valid():
      message.save()
      return Response(message.data)

    else:
      return Response({
        'errors': message.errors
      }, status=status.HTTP_400_BAD_REQUEST)


  def get(self, request):
    messages = Message.objects.filter(
      Q(sender = request.user) | Q(receiver = request.user)
      ).order_by('-created_at')
    m = MessageSerializer(messages, many=True)

    return Response ({
      'data': {
        'messages': m.data
      }
    })


class getMessageView (APIView):

  def get(self, request, id):
    user = User.objects.get(id=id)
    messages = Message.objects.filter(
      (Q(sender = request.user) & Q(receiver = id)) | 
      (Q(receiver = request.user) & Q(sender = id))
      ).order_by('created_at')
    m = MessageSerializer(messages, many=True)
    u = UserSerializer(user)

    return Response ({
      'data': {
        'messages': m.data,
        'user': u.data
      }
    })