from django.urls import path

from . import views

urlpatterns = [
  path('', views.commentView.as_view()),
  path('edit', views.editCommentView.as_view()),
]