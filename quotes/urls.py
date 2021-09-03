from django.urls import path

from . import views

urlpatterns = [
  path('', views.quoteView.as_view()),
  path('edit', views.editQuoteView.as_view())
]