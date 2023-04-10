from django.urls import path

from apps.blog.views import (AddlikeView, BlogDetailView, BlogView,
                             CommentCreateView, CreateBlogPost, DeletePostView,
                             EditPostView, PostsSearchResultView)

app_name = 'blog'

urlpatterns = [
    path('', BlogView.as_view(), name='index'),
    path('category/<str:slug>/', BlogView.as_view(), name='category'),
    path('category/<str:slug>/page/<int:page>/', BlogView.as_view(), name='categorypaginator'),
    path('page/<int:page>/', BlogView.as_view(), name='paginator'),
    path('addlike/<str:slug>/', AddlikeView.as_view(), name='addlike'),
    path('new/', CreateBlogPost.as_view(), name='new'),
    path('search/', PostsSearchResultView.as_view(), name='search'),
    path('<str:slug>/edit/', EditPostView.as_view(), name='edit'),
    path('<str:slug>/delete/', DeletePostView.as_view(), name='delete'),
    path('<str:slug>/', BlogDetailView.as_view(), name='post'),
    path('<str:slug>/comment/<int:parent>', CommentCreateView.as_view(), name='commentcreate'),
]
