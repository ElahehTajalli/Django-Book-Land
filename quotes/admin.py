from django.contrib import admin
from quotes.models import Quote


class QuoteAdmin(admin.ModelAdmin):
  list_display = ('id', 'author', 'text', 'created_at')

admin.site.register(Quote, QuoteAdmin)
