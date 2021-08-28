from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from posts.serializers import *
from books.serializers import UpdateBookSerializer
from users.models import *
from books.models import Book
from posts.models import Post


class postView (APIView):

  def post(self, request):
    book = Book.objects.get(id = request.POST['book'])
    data = {
      'critic': request.POST['user'],
      'book': request.POST['book'],
      'rate': request.POST['rate'],
      'text': request.POST['text']
    }
    post = CreatePostSerializer(
      data = data
    )

    if post.is_valid():
      book = UpdateBookSerializer(book,
        data = request.POST, partial=True)

      if book.is_valid():
        post.save()
        book.save()
        
        self.setAuthorRate(book.data)
        if book.data['translator'] != None:
          self.setTranslatorRate(book.data)

      else:
        return Response({
          'errors': book.errors
        }, status=status.HTTP_400_BAD_REQUEST)

      return Response(post.data)
    else:
      return Response({
        'errors': post.errors
      }, status=status.HTTP_400_BAD_REQUEST)


  def get(self, request):
    posts = []
    if 'user_id' in request.GET:
      user = User.objects.get(id = request.GET['user_id'])
      posts = Post.objects.filter(critic = user).order_by('-created_at')
    if 'book_id' in request.GET:
      book = Book.objects.get(id = request.GET['book_id'])
      posts = Post.objects.filter(book = book).order_by('-created_at')
    
    p = PostSerializer(posts, many=True)

    return Response ({
      'data': {
        'posts': p.data
      }
    })
    
  def setAuthorRate(self, book):
    author = Author.objects.get(
      id = book['author']
    )
    rate = ((author.book_numbers * author.rate) + float(book['rate'])) / (author.book_numbers + 1)
    author.rate = rate
    author.book_numbers = author.book_numbers + 1
    author.save()

  def setTranslatorRate(self, book):
    translator = Translator.objects.get(
      id = book['translator']
    )
    rate = ((translator.book_numbers * translator.rate) + float(book['rate'])) / (translator.book_numbers + 1)
    translator.rate = rate
    translator.book_numbers = translator.book_numbers + 1
    translator.save()


class getPostView (APIView):
  def get (self, request, id):
    p = Post.objects.get(id=id)
    post = PostSerializer(p)
    return Response ({
      'data': {
        'post': post.data
      }
    })


class editPostView (APIView):

  def patch (self, request):
    user = User.objects.get(id = request.data['user'])
    post = Post.objects.get(id = request.data['post'])

    like = Post.objects.filter(id = request.data['post'], likes = request.data['user'])
    if len(like) > 0:
      like[0].likes.remove(user)
      if request.data['action'] == 'like':
        post = PostSerializer(like[0])
        return Response({
        'data': {
          'post': post.data
        }
      }, status=status.HTTP_200_OK)

    dislike = Post.objects.filter(id = request.data['post'], dislikes = request.data['user'])
    if len(dislike) > 0:
      dislike[0].dislikes.remove(user)
      if request.data['action'] == 'dislike':
        post = PostSerializer(dislike[0])
        return Response({
        'data': {
          'post': post.data
        }
      }, status=status.HTTP_200_OK)

    data = {
      'user': request.data['user'],
      'action': request.data['action']
    }
    post = UpdatePostSerializer(post, data = request.data, context = data, partial=True)

    if post.is_valid():
      post.save()
      return Response({
        'data': {
          'post': post.data
        }
      }, status=status.HTTP_200_OK)

    else:
      return Response({
        'errors': post.errors
      }, status=status.HTTP_400_BAD_REQUEST)


class getFollowingPostsView (APIView):
  def get (self, request):
    following = Relationship.objects.filter(following=request.user).values_list('follower', flat=True)
    posts = PostSerializer(Post.objects.filter(critic__id__in=following).order_by('-created_at'), many=True)
    return Response({
      'data': {
        'posts': posts.data,
      }, 'total': len(posts.data)
    }, status=status.HTTP_200_OK)