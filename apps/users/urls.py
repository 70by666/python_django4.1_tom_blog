from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.users.views import (ChangePasswordView, EmailVerificationFailedView,
                              EmailVerificationView, FailedSetPasswordView,
                              LoginView, ProfileAllPostsView,
                              ProfileCommentCreateView, ProfileEditView,
                              ProfileView, RegisterView, ResetPasswordView,
                              SetPasswordView, TelegramView, TgFailedView)

app_name = 'users'

urlpatterns = [
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    path('profile/<str:slug>/commentcreate/', ProfileCommentCreateView.as_view(), name='profilecommentcreate'),
    path('profile/<str:slug>/all/', ProfileAllPostsView.as_view(), name='allposts'),
    path('profile/<str:slug>/all/<int:page>/', ProfileAllPostsView.as_view(), name='paginator_profile'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email'),
    path('verifyfailed/', EmailVerificationFailedView.as_view(), name='email_failed'),
    path('resetpassword/', ResetPasswordView.as_view(), name='resetpassword'),
    path('setpassword/<uidb64>/<token>/', SetPasswordView.as_view(), name='setpassword'),
    path('failedsetpassword/', FailedSetPasswordView.as_view(), name='failedsetpassword'),
    path('tgverify/<int:tg_id>/<uuid:code>/', TelegramView.as_view(), name='tgverify'),
    path('tg_failed/', TgFailedView.as_view(), name='tg_failed'),   
]
