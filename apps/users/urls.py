from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.users.views import (ChangePasswordView, EmailVerificationFailedView,
                              EmailVerificationView, LoginView,
                              ProfileEditView, ProfileView, RegisterView, 
                              ProfileAllPostsView)

app_name = 'users'

urlpatterns = [
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    path('profile/<str:slug>/all', ProfileAllPostsView.as_view(), name='allposts'),
    path('profile/<str:slug>/all/<int:page>/', ProfileAllPostsView.as_view(), name='paginator_profile'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email'),
    path('verifyfailed/', EmailVerificationFailedView.as_view(), name='email_failed'),
]
