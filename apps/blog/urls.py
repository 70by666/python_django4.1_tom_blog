from django.urls import path

from apps.blog.views import AddlikeView, BlogDetailView, BlogView

app_name = 'blog'

urlpatterns = [
    path('', BlogView.as_view(), name='index'),
    path('post/<str:slug>', BlogDetailView.as_view(), name='post'),
    path('category/<str:slug>', BlogView.as_view(), name='category'),
    path('page/<int:page>', BlogView.as_view(), name='paginator'),
    path('addlike/<str:slug>', AddlikeView.as_view(), name='addlike'),
]
