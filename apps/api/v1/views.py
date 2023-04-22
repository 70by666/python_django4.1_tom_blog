import uuid
from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.api.v1.models import TgAuth
from apps.api.v1.permissions import IsSuperUser
from apps.api.v1.serializator import PostsSerializer, UserSerializer
from apps.blog.models import Posts
from apps.users.models import User


class BlogViewSet(ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsSuperUser,)


class GetUserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)

    def get_object(self):
        user_id = self.kwargs['user_id']
        obj = User.objects.filter(tg_id=user_id)
        
        return obj.first()


class UrlAuthAPIView(APIView):
    def get(self, request, user_id):
        code = uuid.uuid4()
        expiration = now() + timedelta(hours=24)
        tg_obj = TgAuth.objects.filter(tg_id=user_id).order_by('-expiration')
        if tg_obj.exists():
            for i in tg_obj:
                if i.is_expired():
                    return Response({
                        'url_auth': 'У вас уже есть действующая ссылка'
                    })
                
        TgAuth.objects.create(
            code=code, 
            tg_id=user_id, 
            expiration=expiration,
        )
        url = f'{settings.DOMAIN_NAME}/users/tgverify/{user_id}/{code}/'
        
        return Response({'url_auth': url})
