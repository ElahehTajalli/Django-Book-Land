from django.contrib.auth import authenticate, login 
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, QueryDict
from django.template.loader import get_template

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from users.serializers import *
from users.models import Verification, Author, Translator, User, Relationship

from random import randint
from django.core.mail import send_mail,EmailMessage
from projectBack.settings import EMAIL_HOST_USER

from django.db.models import Max


class loginView(APIView):
  permission_classes = [AllowAny]
  def post (self, request):
    user = authenticate(
    request = request,
    email = request.POST['email'],
    password = request.POST['password'])

    if user:
      token, _ = Token.objects.get_or_create(user=user)
      login(request, user)
      return Response({
        'token': token.key
      })
    else:
      return Response({
        'errors': 'Email or password is wrong!'
      }, status = status.HTTP_404_NOT_FOUND)


class registerView(APIView):
  permission_classes = [AllowAny]
  def post (self, request):
    # Delete an inactive existing user
    try:
      user = User.objects.get(email = request.POST['email'])
      if (user.is_active == False):
        user.delete()

    finally:
      last_user_id = User.objects.aggregate(max=Max('id'))
      user = CreateUserSerializer(data= request.POST, context= 'کتابخوان' + ' ' + str(last_user_id['max']))
      if user.is_valid():
        user.save()
                
        content = {
          'email': user.data['email']
        }
                
        subject = 'کد فعال سازی حساب'
        message = get_template('activation_code.html').render(content)
                
        email = EmailMessage(subject, message, EMAIL_HOST_USER,
          [str(user.instance.email)])
        email.content_subtype = "html"
        email.send()
        
        return Response({
          'message': 'Verification link sent to your email'
        }, status = status.HTTP_200_OK)

      else:
        return Response({
          'errors': user.errors
        }, status = status.HTTP_400_BAD_REQUEST)


# Find user to change password
class FoundUser(APIView):
  permission_classes = [AllowAny]
  def post(self, request):
    try:
      user = User.objects.get(email = request.POST['email'])
      verification = Verification.objects.get(user = user)

      code = randint(10000, 99999)
      data = {
        'code': code
      }
      verification = UpdateVerificationSerializer(verification, data = data, context = data, partial=True)
      if verification.is_valid():
        verification.save()

        #send verification code to email
        email = EmailMessage('Verification Code', str(verification.data['code']), EMAIL_HOST_USER,
        [str(user.email)])
        email.send()

        return Response({
          'message': 'Verification code sent to your email'
        }, status = status.HTTP_200_OK)
      else:
        return Response({
          'errors': verification.errors
        }, status = status.HTTP_400_BAD_REQUEST)

    except:
      return Response({
        'errors': 'email_not_found'
      }, status = status.HTTP_404_NOT_FOUND)  


class ForgotPasswordView(APIView):
  permission_classes = [AllowAny]
  def patch (self, request):
    user = UpdateUserSerializer(User.objects.get(email = request.data['email']),
      data = request.data, partial=True)

    if user.is_valid():
      user.save()
      user = User.objects.get(
        email = request.data['email']
      )
      token, _ = Token.objects.get_or_create(user=user)
      login(request, user)
      return Response({
        'token': token.key
      }, status = status.HTTP_200_OK)

    else:
      return Response({
        'errors': user.errors
      }, status = status.HTTP_400_BAD_REQUEST)    


class CheckVerificationView (APIView):
  permission_classes = [AllowAny]
  def post(self, request):
    u = User.objects.get(
      email = request.data['email']
    )
    v = Verification.objects.get(
      user = u
    )
    if v.code == request.data['code']:
      token, _ = Token.objects.get_or_create(user = u)
      u.is_active = True
      u.save()

      login(request, u)

      return Response({
        'token': token.key,
        'message': 'Verification code is correct.'
      }, status = status.HTTP_200_OK)
    else:
      return Response({
        'errors': 'Please insert the correct code'
      }, status = status.HTTP_400_BAD_REQUEST)



class selfView(APIView):
  def get (self, request):
    user = request.user
    u = UserSerializer(user)
    return Response ({
      'data': u.data
    })


class getAuthorsView(APIView):
  permission_classes = [AllowAny]
  def get (self, request):
    try:
      count = int(request.GET['count'])
      if (request.GET['sort'].split(':')[1] == 'asc'):
        author = AuthorSerializer(
          Author.objects.all().order_by(request.GET['sort'].split(':')[0])[:count],
          many=True
        )
      else:
        author = AuthorSerializer(
          Author.objects.all().order_by('-'+request.GET['sort'].split(':')[0])[:count],
          many=True,
        )
    except:
      if (request.GET['sort'].split(':')[1] == 'asc'):
        author = AuthorSerializer(
          Author.objects.all().order_by(request.GET['sort'].split(':')[0]),
          many=True
        )
      else:
        author = AuthorSerializer(
          Author.objects.all().order_by('-'+request.GET['sort'].split(':')[0]),
          many=True,
        )
    return JsonResponse({
      'data': {
        'authors': author.data
      },
      'total': len(author.data)
    })


class getTranslatorsView(APIView):
  permission_classes = [AllowAny]
  def get (self, request):
    try:
      count = int(request.GET['count'])
      if (request.GET['sort'].split(':')[1] == 'asc'):
        translator = TranslatorSerializer(
          Translator.objects.all().order_by(request.GET['sort'].split(':')[0])[:count],
          many=True
        )
      else:
        translator = TranslatorSerializer(
          Translator.objects.all().order_by('-'+request.GET['sort'].split(':')[0])[:count],
          many=True,
        )
    except:
      if (request.GET['sort'].split(':')[1] == 'asc'):
        translator = TranslatorSerializer(
          Translator.objects.all().order_by(request.GET['sort'].split(':')[0]),
          many=True
        )
      else:
        translator = TranslatorSerializer(
          Translator.objects.all().order_by('-'+request.GET['sort'].split(':')[0]),
          many=True,
        )
    return JsonResponse({
      'data': {
        'translators': translator.data
      },
      'total': len(translator.data)
    })


class getUserView(APIView):
  def get (self, request, id):
    u = User.objects.get(id=id)
    user = UserSerializer(u)
    return Response ({
      'data': {
        'user': user.data
      }
    })


class followView(APIView):
  def post(self, request):
    relationship = CreateRelationshipSerializer(data = request.POST)

    if relationship.is_valid():
      relationship.save()
      return Response(relationship.data)
    else:
      return Response({
        'errors': relationship.errors
      }, status=status.HTTP_400_BAD_REQUEST)


class unfollowView(APIView):
  def post(self, request):
    try:
      relationship = Relationship.objects.get(following = request.POST['following'], follower = request.POST['follower'])
      relationship.delete()
      return Response(status=status.HTTP_200_OK)
    except:
      return Response({
        'errors': relationship.errors
      }, status=status.HTTP_400_BAD_REQUEST)

      
class checkRelationshipView(APIView):
  def post(self, request):
    relationship = Relationship.objects.filter(following = request.POST['following'], follower = request.POST['follower'])

    if len(relationship) > 0:
      return Response(status=status.HTTP_200_OK)

    else:
      return Response(status=status.HTTP_404_NOT_FOUND)


class getRelationshipsView(APIView):
  def get(self, request):
    relationships = []
    if 'follower_id' in request.GET:
      relationships = Relationship.objects.filter(follower = request.GET['follower_id'])
    if 'following_id' in request.GET:
      relationships = Relationship.objects.filter(following = request.GET['following_id'])
    
    r = RelationshipSerializer(relationships, many=True)

    return Response ({
      'data': {
        'relationships': r.data
      },
      'total': len(r.data)
    })

class editView(APIView):
  def patch (self, request):
    user = EditUserSerializer(User.objects.get(email = request.data['email']),
      data = request.data, partial=True)

    if user.is_valid():
      user.save()
      return Response({
        'data': user.data
      }, status = status.HTTP_200_OK)   
    else:
      return Response({
        'errors': user.errors
      }, status = status.HTTP_400_BAD_REQUEST)   
      

class editInfoView(APIView):
  permission_classes = [AllowAny]
  def patch (self, request):
    user = CompleteInfoUserSerializer(User.objects.get(email = request.data['email']),
      data = request.data, partial=True)

    if user.is_valid():
      user.save()
      
      token, _ = Token.objects.get_or_create(user = user.instance)
      user.instance.is_active = True
      
      user.save()
      login(request, user.instance)

      return Response({
        'token': token.key,
      }, status = status.HTTP_200_OK)
    else:
      return Response({
        'errors': user.errors
      }, status = status.HTTP_400_BAD_REQUEST)