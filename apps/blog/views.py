from django.views.generic import ListView

from apps.blog.models import Posts
from common.views import CommonContextMixin

class BlogView(CommonContextMixin, ListView):
    model = Posts
    template_name = 'blog/blog.html'
    title = 'Блог'
