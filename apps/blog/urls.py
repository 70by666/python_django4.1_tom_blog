from django.urls import path

from apps.blog.views import BlogDetailView, BlogView

app_name = 'blog'

urlpatterns = [
    path('', BlogView.as_view(), name='index'),
    path('post/<str:slug>', BlogDetailView.as_view(), name='post'),
    path('category/<str:slug>', BlogView.as_view(), name='category'),

]
