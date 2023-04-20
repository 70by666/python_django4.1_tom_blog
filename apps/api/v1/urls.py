from django.urls import include, path
from rest_framework import routers

from apps.api.v1.views import BlogViewSet

app_name = 'api.v1'

router = routers.DefaultRouter()
router.register('products', BlogViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),

]
