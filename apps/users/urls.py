from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.users.views import (LoginView, ProfileEditView, ProfileView,
                              RegisterView)

app_name = 'users'

urlpatterns = [
    path('profile/<str:slug>', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]
