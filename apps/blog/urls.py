from django.urls import path

from apps.blog.views import BlogView


app_name = 'blog'

urlpatterns = [
    path('', BlogView.as_view(), name='index')
]
