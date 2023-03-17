from django.urls import path

from apps.users.views import ProfileView, ProfileEditView

app_name = 'users'

urlpatterns = [
    path('profile/<str:slug>', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
]
