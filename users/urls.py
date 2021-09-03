from django.urls import path

from . import views

urlpatterns = [
  path('login', views.loginView.as_view()),
  path('register', views.registerView.as_view()),
  path('forgot_password', views.ForgotPasswordView.as_view()),
  path('edit', views.editView.as_view()),
  path('edit_info', views.editInfoView.as_view()),
  path('found_user', views.FoundUser.as_view()),
  path('check_verification', views.CheckVerificationView.as_view()),
  path('self',views.selfView.as_view()),
  path('get_authors',views.getAuthorsView.as_view()),
  path('get_translators',views.getTranslatorsView.as_view()),
  path('<int:id>/', views.getUserView.as_view()),
  path('follow', views.followView.as_view()),
  path('unfollow', views.unfollowView.as_view()),
  path('checkRelationship', views.checkRelationshipView.as_view()),
  path('getRelationships', views.getRelationshipsView.as_view())
]