from django.contrib import admin
from books.models import *


class BookAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'author', 'publisher', 'rate', 'created_at', 'translator')

admin.site.register(Book, BookAdmin)

class RateAdmin(admin.ModelAdmin):
  list_display = ('user', 'book', 'rate')

admin.site.register(Rate, RateAdmin)

class PlanAdmin(admin.ModelAdmin):
  list_display = ('id', 'user')
  
admin.site.register(Plan, PlanAdmin)
  
class FavoriteAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'book')

admin.site.register(Favorite, FavoriteAdmin)
