from django.urls import include, path
from rest_framework import routers

from apps.api.v1.views import (BlogViewSet, GetUserRetrieveAPIView,
                               UrlAuthAPIView)

app_name = 'api.v1'

router = routers.DefaultRouter()
router.register('products', BlogViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:user_id>/', GetUserRetrieveAPIView.as_view()),
    path('geturl/<int:user_id>/', UrlAuthAPIView.as_view()),   
]
