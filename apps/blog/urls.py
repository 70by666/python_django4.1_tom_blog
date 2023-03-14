from django.urls import path

from apps.blog.views import BlogView, BlogDetailView


app_name = 'blog'

urlpatterns = [
    path('', BlogView.as_view(), name='index'),
    path('post/<str:slug>', BlogDetailView.as_view(), name='post'),
]
