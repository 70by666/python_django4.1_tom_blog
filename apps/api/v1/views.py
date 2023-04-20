from rest_framework.viewsets import ModelViewSet

from apps.api.v1.permissions import IsSuperUser


class BlogViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsSuperUser,)
