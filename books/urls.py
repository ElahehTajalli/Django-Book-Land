from django.urls import path

from . import views

urlpatterns = [
  path('add', views.addBookView.as_view()),
  path('list', views.getBooksView.as_view()),
  path('<int:id>/', views.getBookView.as_view()),
  path('rate', views.rateView.as_view()),
  path('plan', views.planView.as_view()),
  path('favorite', views.favoriteView.as_view()),
  path('getPlan', views.getPlanView.as_view()),
  path('getFavorite', views.getFavoriteView.as_view())
]
