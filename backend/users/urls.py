from django.urls import path, include
from rest_framework import routers

from .views import UsersViewSet


router = routers.DefaultRouter()

router.register(r'users', UsersViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
