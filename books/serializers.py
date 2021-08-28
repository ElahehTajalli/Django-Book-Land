from books.models import Book, Rate, Plan, Favorite
from users.models import User
from rest_framework import serializers
from users.serializers import AuthorSerializer, TranslatorSerializer, UserSerializer

class BookSerializer(serializers.ModelSerializer):
  author = AuthorSerializer()
  translator = TranslatorSerializer()

  class Meta:
    model = Book
    fields = '__all__'


class CreateBookSerializer(serializers.ModelSerializer):

  class Meta:
    model = Book
    fields = '__all__'


# def create(self, validated_data):
#     a = Author.objects.get(
#       id = b.data['author']
#     )
#     t = Translator.objects.get(
#       id = b.data['translator']
#     )
#     book = Author(
#       name = validated_data['name'],
#       author = a,
#       publisher = validated_data['publisher'],
#       genre = validated_data['genre'],
#       rate = validated_data['rate'],
#       publication_year = validated_data['publication_year'],
#       translator = t,
#       image = validated_data['image'],
#       summary = validated_data['summary']
#     )
#     book.save()
#     return book


class UpdateBookSerializer(serializers.ModelSerializer):

  class Meta:
    model = Book
    fields = '__all__'

  def update(self, instance, validated_data):
    
    old_rate = instance.rate
    old_rate_numbers = instance.rate_numbers
    new_rate_numbers = old_rate_numbers + 1
    new_rate = ((old_rate_numbers * old_rate) + validated_data['rate']) / new_rate_numbers

    instance.rate = new_rate
    instance.rate_numbers = new_rate_numbers
    instance.save()
    return instance


class CreateRateSerializer(serializers.ModelSerializer):

  class Meta:
    model = Rate
    fields = '__all__'


class CreatePlanSerializer(serializers.ModelSerializer):

  class Meta:
    model = Plan
    fields = '__all__'

  def create(self, validated_data):
    book = Book.objects.get(
      id = self.context['book']
    )
    p = Plan(
      user = validated_data['user']
    )
    p.save()
    if self.context['list'] == 'read':
      p.read.add(book)
    if self.context['list'] == 'reading':
      p.reading.add(book)
    if self.context['list'] == 'wants_to_read':
      p.wants_to_read.add(book)

    p.save()
    return p


class UpdatePlanSerializer(serializers.ModelSerializer):

  class Meta:
    model = Plan
    fields = '__all__'

  def update(self, instance, validated_data):
    book = Book.objects.get(
      id = self.context['book']
    )
    if self.context['list'] == 'read':
      instance[0].read.add(book)
    if self.context['list'] == 'reading':
      instance[0].reading.add(book)
    if self.context['list'] == 'wants_to_read':
      instance[0].wants_to_read.add(book)

    instance[0].save()
    return instance[0]



class PlanSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  read = BookSerializer(many=True)
  reading = BookSerializer(many=True)
  wants_to_read = BookSerializer(many=True)

  class Meta:
    model = Plan
    fields = '__all__'
    
    
class FavoriteSerializer(serializers.ModelSerializer):
  book = BookSerializer()
  user = UserSerializer()

  class Meta:
    model = Favorite
    fields = '__all__'

    
class CreateFavoriteSerializer(serializers.ModelSerializer):

  class Meta:
    model = Favorite
    fields = '__all__'