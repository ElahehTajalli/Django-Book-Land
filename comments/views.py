from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from comments.serializers import *
from books.serializers import UpdateBookSerializer
from users.models import User
from books.models import Book
from posts.models import Post
from comments.models import Comment


class commentView (APIView):

  def post(self, request):
    data = {
      'post': request.POST['post_id'],
      'user': request.POST['user_id'],
      'text': request.POST['text']
    }
    comment = CreateCommentSerializer(
      data = data
    )

    if comment.is_valid():
      comment.save()
      return Response(comment.data)

    else:
      return Response({
        'errors': comment.errors
      }, status=status.HTTP_400_BAD_REQUEST)


  def get(self, request):
    comments = []
    if 'user_id' in request.GET:
      user = User.objects.get(id = request.GET['user_id'])
      comments = Comment.objects.filter(user = user).order_by('-created_at')
    if 'post_id' in request.GET:
      post = Post.objects.get(id = request.GET['post_id'])
      comments = Comment.objects.filter(post = post).order_by('-created_at')
    
    c = CommentSerializer(comments, many=True)

    return Response ({
      'data': {
        'comments': c.data
      }
    })


class editCommentView (APIView):

  def patch (self, request):
    user = User.objects.get(id = request.data['user'])
    comment = Comment.objects.get(id = request.data['comment'])

    like = Comment.objects.filter(id = request.data['comment'], likes = request.data['user'])
    if len(like) > 0:
      like[0].likes.remove(user)
      if request.data['action'] == 'like':
        comment = CommentSerializer(like[0])
        return Response({
          'data': {
            'comment': comment.data
          }
        },status=status.HTTP_200_OK)

    dislike = Comment.objects.filter(id = request.data['comment'], dislikes = request.data['user'])
    if len(dislike) > 0:
      print(dislike)
      dislike[0].dislikes.remove(user)
      if request.data['action'] == 'dislike':
        comment = CommentSerializer(dislike[0])
        return Response({
        'data': {
          'comment': comment.data
        }
      },status=status.HTTP_200_OK)

    data = {
      'user': request.data['user'],
      'action': request.data['action']
    }
    comment = UpdateCommentSerializer(comment, data = request.data, context = data, partial=True)

    if comment.is_valid():
      comment.save()
      return Response({
        'data': {
          'comment': comment.data
        }
      }, status=status.HTTP_200_OK)

    else:
      return Response({
        'errors': comment.errors
      }, status=status.HTTP_400_BAD_REQUEST)



