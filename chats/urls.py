from django.urls import path

from . import views

urlpatterns = [
  path('', views.messageView.as_view()),
  path('<int:id>/', views.getMessageView.as_view()),
]