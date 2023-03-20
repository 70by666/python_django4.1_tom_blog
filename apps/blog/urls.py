from django.urls import path

from apps.blog.views import AddlikeView, BlogDetailView, BlogView, CreateBlogPost

app_name = 'blog'

urlpatterns = [
    path('', BlogView.as_view(), name='index'),
    path('category/<str:slug>/', BlogView.as_view(), name='category'),
    path('page/<int:page>/', BlogView.as_view(), name='paginator'),
    path('addlike/<str:slug>/', AddlikeView.as_view(), name='addlike'),
    path('new/', CreateBlogPost.as_view(), name='new'),
    path('<str:slug>/', BlogDetailView.as_view(), name='post'),
]
