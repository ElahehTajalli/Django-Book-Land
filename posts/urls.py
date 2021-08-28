from django.urls import path

from . import views

urlpatterns = [
  path('', views.postView.as_view()),
  path('<int:id>/', views.getPostView.as_view()),
  path('edit', views.editPostView.as_view()),
  path('getPosts', views.getFollowingPostsView.as_view())
  
]