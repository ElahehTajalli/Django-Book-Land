from django.contrib.auth import authenticate, login 
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, QueryDict
from django.core import serializers

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from books.serializers import *
from books.models import Book, Rate, Plan

from users.serializers import TranslatorSerializer, AuthorSerializer
from users.models import Author, Translator

from django.shortcuts import render

class addBookView(APIView):

  def post (self, request):
    req = request.data.copy()

    response = CreateBookSerializer(
      data = req
    )
    if response.is_valid():
      response.save()
      
      return Response(response.data)

    else:
      # If author not exist create author then create book
      if 'author' in response.errors:
        name = 'author'
        req = self.createAuthorOrTranslator(req, name)

      # If translator not exist create translator then create book
      if 'translator' in response.data and response.data['translator'] != None:
        if 'translator' in response.errors:
          name = 'translator'
          req = self.createAuthorOrTranslator(req, name)
        
      response = CreateBookSerializer(
        data = req
      )
      if response.is_valid():
        response.save()
        return Response(response.data)
      else:
        return Response({
          'errors': response.errors
        }, status=status.HTTP_400_BAD_REQUEST)


  def createAuthorOrTranslator(self, request, name):
    data = {
      'name': request[name],
    }
    if name == 'author':
      response = AuthorSerializer(
        data = data
      )
    else:
      response = TranslatorSerializer(
        data = data
      )
    if response.is_valid():
      response.save()
      data = request
      data[name] = response.data['id']
      return data

    return Response({
      'errors': response.errors
    }, status=status.HTTP_400_BAD_REQUEST)


class getBooksView(APIView):
  permission_classes = [AllowAny]
  def get (self, request):
    sort = request.GET['sort']
    books = Book.objects.all()

    if 'authors' in request.GET:
      authors = request.GET.getlist('authors')
      books = books.filter(author__name__in = authors)

    if 'translators' in request.GET:
      translators = request.GET.getlist('translators')
      books = books.filter(translator__name__in = translators)

    if 'genre' in request.GET:
      genre = request.GET['genre']
      books = books.filter(genre__icontains=genre)

    if 'publisher' in request.GET:
      publisher = request.GET['publisher']
      books = books.filter(publisher__icontains = publisher)

    try:
      count = int(request.GET['count'])
      if (sort.split(':')[1] == 'asc'):
        books = books.order_by(sort.split(':')[0])[:count]
      else:
        books = books.order_by('-'+sort.split(':')[0])[:count]

    except:
      if (sort.split(':')[1] == 'asc'):
        books = books.order_by(sort.split(':')[0])
      else:
        books = books.order_by('-'+sort.split(':')[0])

    books = BookSerializer(books, many=True)
    return JsonResponse({
      'data': {
        'books': books.data
      },
      'total': len(books.data)
    })



class getBooksByFilterView(APIView):
  permission_classes = [AllowAny]
  def get (self, request):
    try:
      count = int(request.GET['count'])
      if (request.GET['sort'].split(':')[1] == 'asc'):
        b = BookSerializer(
          Book.objects.all().order_by(request.GET['sort'].split(':')[0])[:count],
          many=True
        )
      else:
        b = BookSerializer(
          Book.objects.all().order_by('-'+request.GET['sort'].split(':')[0])[:count],
          many=True,
        )
    except:
      if (request.GET['sort'].split(':')[1] == 'asc'):
        b = BookSerializer(
          Book.objects.all().order_by(request.GET['sort'].split(':')[0]),
          many=True
        )
      else:
        b = BookSerializer(
          Book.objects.all().order_by('-'+request.GET['sort'].split(':')[0]),
          many=True,
        )
    return JsonResponse({
      'data': {
        'books': b.data
      },
      'total': len(b.data)
    })


class getBookView(APIView):
  permission_classes = [AllowAny]
  def get (self, request, id):
    b = Book.objects.get(id=id)
    book = BookSerializer(b)
    return Response ({
      'data': book.data
    })


class rateView(APIView):
  def post (self, request):
    rate = Rate.objects.filter(user = request.POST['user'], book = request.POST['book'])

    if len(rate) > 0:
      return Response({
        'errors': 'you_have_already_voted_for_this_book'
      },status=status.HTTP_400_BAD_REQUEST)

    else:
      rate = CreateRateSerializer(data = request.POST)
      book = Book.objects.get(id = request.POST['book'])
      if rate.is_valid():
        book = UpdateBookSerializer(book,
          data = request.POST, partial=True)

        if book.is_valid():
          rate.save()
          book.save()
          
          self.setAuthorRate(book.data)
          if book.data['translator'] != None:
            self.setTranslatorRate(book.data)

        else:
          return Response({
            'errors': book.errors
          }, status=status.HTTP_400_BAD_REQUEST)

        return Response(book.data)

      else:
        return Response({
          'errors': rate.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
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


  # def get(self, request):
  # rate = Rate.objects.filter(user = request.GET['user'], book = request.GET['book'])

  # if len(rate) > 0:
  #   return Response(status=status.HTTP_200_OK)

  # else:
  #   return Response(status=status.HTTP_404_NOT_FOUND)


class planView(APIView):
  def post (self, request):

    book = Book.objects.get(id = request.POST['book'])
    plan = Plan.objects.filter(user = request.POST['user'])

    # if plan exist, update it
    if len(plan) > 0:
      read = Plan.objects.filter(user = request.POST['user'], read = request.POST['book'])
      reading = Plan.objects.filter(user = request.POST['user'], reading = request.POST['book'])
      wants_to_read = Plan.objects.filter(user = request.POST['user'], wants_to_read = request.POST['book'])

      # Delete book from lists
      if len(read) > 0:
        read[0].read.remove(book)
        if request.POST['list'] == 'read':
          return Response(status=status.HTTP_200_OK)

      if len(reading) > 0:
        reading[0].reading.remove(book)
        if request.POST['list'] == 'reading':
          return Response(status=status.HTTP_200_OK)

      if len(wants_to_read) > 0:
        wants_to_read[0].wants_to_read.remove(book)
        if request.POST['list'] == 'wants_to_read':
          return Response(status=status.HTTP_200_OK)

      data = {
        'book': request.POST['book'],
        'list': request.POST['list']
      }
      plan = UpdatePlanSerializer(plan, data = request.POST, context = data, partial=True)

      if plan.is_valid():
        plan.save()
        return Response(plan.data, status=status.HTTP_200_OK)

      else:
        return Response({
          'errors': plan.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # if plan not exist
    else:
      data = {
        'book': request.POST['book'],
        'list': request.POST['list']
      }
      plan = CreatePlanSerializer(data = request.POST, context= data)

      if plan.is_valid():
        plan.save()
        return Response(plan.data, status=status.HTTP_200_OK)

      else:
        return Response({
          'errors': plan.errors
        }, status=status.HTTP_400_BAD_REQUEST)


  def get(self, request):
    plan = Plan.objects.filter(user = request.GET['user'])

    if len(plan) > 0:
      read = Plan.objects.filter(user = request.GET['user'], read = request.GET['book'])
      if len(read) > 0:
        return Response({
          'isRead': True,
          'isReading': False,
          'isWantsToRead': False
        },status=status.HTTP_200_OK)

      reading = Plan.objects.filter(user = request.GET['user'], reading = request.GET['book'])
      if len(reading) > 0:
        return Response({
          'isRead': False,
          'isReading': True,
          'isWantsToRead': False
        },status=status.HTTP_200_OK)

      wants_to_read = Plan.objects.filter(user = request.GET['user'], wants_to_read = request.GET['book'])
      if len(wants_to_read) > 0:
        return Response({
          'isRead': False,
          'isReading': False,
          'isWantsToRead': True
        },status=status.HTTP_200_OK)
        
      return Response({
          'isRead': False,
          'isReading': False,
          'isWantsToRead': False
        },status=status.HTTP_200_OK)

    else:
      return Response({
          'isRead': False,
          'isReading': False,
          'isWantsToRead': False
        }, status=status.HTTP_404_NOT_FOUND)
      
      
class getPlanView(APIView):
  def get(self, request):
    try:
      plan = Plan.objects.get(user = request.GET['user'])
      plan = PlanSerializer(plan)
      return Response({
        'data': {
          'plan': plan.data
        }
      },status=status.HTTP_200_OK)
    except:
      return Response(status=status.HTTP_404_NOT_FOUND)



class favoriteView(APIView):
  def post (self, request):
    favorite = Favorite.objects.filter(user = request.user, book = request.POST['book'])
    
    if len(favorite) > 0:
      r = FavoriteSerializer(favorite[0])
      favorite[0].delete()
      return Response(r.data, status=status.HTTP_200_OK)
    
    data = {
      'user': request.user.id,
      'book': request.POST['book']
    }
    favorite = CreateFavoriteSerializer(data = data)
    
    if favorite.is_valid():
      favorite.save()
      return Response(favorite.data, status=status.HTTP_200_OK)
    
    else:
      return Response({
        'errors': favorite.errors
      }, status=status.HTTP_400_BAD_REQUEST)
      
  def get (self, request):
    favorite = Favorite.objects.filter(user = request.user, book = request.GET['book'])
    
    if len(favorite) > 0:
      r = FavoriteSerializer(favorite[0])
      print(r)
      return Response ({
        'data': {
          'favorite': r.data
        }
      })
    else:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
class getFavoriteView(APIView):
  def get(self, request):
    favorite = Favorite.objects.filter(user = request.GET['user']).values_list('book')
    
    if len(favorite) > 0:
      book = Book.objects.filter(id__in = favorite)
      book = BookSerializer(book, many=True)
      return Response({
        'data': {
          'favorite': book.data
        }
      },status=status.HTTP_200_OK)
    else:
      return Response(status=status.HTTP_404_NOT_FOUND)