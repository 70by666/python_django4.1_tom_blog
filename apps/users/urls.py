from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.users.views import (LoginView, ProfileEditView, ProfileView,
                              RegisterView, ChangePasswordView)

app_name = 'users'

urlpatterns = [
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]
