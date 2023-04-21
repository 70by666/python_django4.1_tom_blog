from rest_framework.viewsets import ModelViewSet

from apps.api.v1.permissions import IsSuperUser
from apps.api.v1.serializator import PostsSerializer
from apps.blog.models import Posts


class BlogViewSet(ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsSuperUser,)
