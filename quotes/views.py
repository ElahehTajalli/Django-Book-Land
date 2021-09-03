from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from quotes.serializers import *
from books.serializers import UpdateBookSerializer
from users.models import User
from books.models import Book
from posts.models import Post
from quotes.models import Quote


class quoteView (APIView):

  def post(self, request):
    quote = QuoteSerializer(
      data = request.data
    )

    if quote.is_valid():
      quote.save()
      return Response(quote.data)

    else:
      return Response({
        'errors': quote.errors
      }, status=status.HTTP_400_BAD_REQUEST)


  permission_classes = [AllowAny]
  def get(self, request):
    quotes = Quote.objects.all().order_by('-created_at')
    q = QuoteSerializer(quotes, many=True)

    return Response ({
      'data': {
        'quotes': q.data
      }
    })


class editQuoteView (APIView):

  def patch (self, request):
    user = User.objects.get(id = request.data['user'])
    quote = Quote.objects.get(id = request.data['quote'])

    like = Quote.objects.filter(id = request.data['quote'], likes = request.data['user'])
    if len(like) > 0:
      like[0].likes.remove(user)
      quote = QuoteSerializer(like[0])
      return Response({
        'data': {
          'quote': quote.data
        }
      },status=status.HTTP_200_OK)

    data = {
      'user': request.data['user'],
    }
    quote = UpdateQuoteSerializer(quote, data = request.data, context = data, partial=True)

    if quote.is_valid():
      quote.save()
      return Response({
        'data': {
          'quote': quote.data
        }
      }, status=status.HTTP_200_OK)

    else:
      return Response({
        'errors': quote.errors
      }, status=status.HTTP_400_BAD_REQUEST)



