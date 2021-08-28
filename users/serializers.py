
from rest_framework import serializers
# from django.contrib.auth.models import User
from users.models import Verification, Author, Translator, User, Relationship


class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ['id', 'email', 'persian_username', 'first_name', 'last_name', 'image']


class UpdateUserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = '__all__'

  def update(self, instance, validated_data):
    instance.set_password(validated_data.get('password', instance.password))
    instance.save()
    return instance
    

class CreateUserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ['email', 'password', 'first_name', 'last_name', 'image']
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = User(
      email=validated_data['email'],
      persian_username=self.context,
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name']
    )
    user.set_password(validated_data['password'])
    user.is_active = False
    user.save()
    return user


class EditUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['email', 'persian_username', 'password', 'first_name', 'last_name', 'image']
    extra_kwargs = {'password': {'write_only': True}}

  def update(self, instance, validated_data):
    instance.first_name = validated_data.get('first_name', instance.first_name)
    instance.last_name = validated_data.get('last_name', instance.last_name)
    instance.persian_username = validated_data.get('persian_username', instance.persian_username)
    if 'image' in validated_data:
      instance.image = validated_data.get('image', instance.image)
    if 'password' in validated_data:
      instance.set_password(validated_data.get('password', instance.password))
    instance.save()
    return instance


class CreateVerificationSerializer(serializers.ModelSerializer):

  class Meta:
    model = Verification
    fields = '__all__'

  def create(self, validated_data):
    verification = Verification(
      user=self.context['user'],
      code=validated_data['code']
    )
    verification.save()
    return verification

class UpdateVerificationSerializer(serializers.ModelSerializer):

  class Meta:
    model = Verification
    fields = '__all__'

  def update(self, instance, validated_data):
    instance.code = validated_data['code']
    instance.save()
    return instance


class AuthorSerializer(serializers.ModelSerializer):

  class Meta:
    model = Author
    fields = '__all__'


# class CreateAuthorSerializer(serializers.ModelSerializer):

  # def create(self, validated_data):
  #   author = Author(
  #     name=validated_data['name'],
  #     rate=validated_data['rate']
  #   )
  #   author.save()
  #   return author

  # class Meta:
  #   model = Author
  #   fields = '__all__'


class TranslatorSerializer(serializers.ModelSerializer):

  class Meta:
    model = Translator
    fields = '__all__'


class RelationshipSerializer(serializers.ModelSerializer):
  following = UserSerializer()
  follower = UserSerializer()

  class Meta:
    model = Relationship
    fields = '__all__'


class CreateRelationshipSerializer(serializers.ModelSerializer):

  class Meta:
    model = Relationship
    fields = '__all__'