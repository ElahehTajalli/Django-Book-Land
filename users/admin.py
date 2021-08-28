from django.contrib import admin
from users.models import Verification, Author, Translator, User, Relationship

class VerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code')

admin.site.register(Verification, VerificationAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rate')

admin.site.register(Author, AuthorAdmin)

class TranslatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rate')

admin.site.register(Translator, TranslatorAdmin)

class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')

admin.site.register(Relationship, RelationshipAdmin)

admin.site.register(User)
