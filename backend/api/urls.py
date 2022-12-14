from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = routers.DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients'),
router.register('tags', TagViewSet, basename='tags'),
router.register('recipes', RecipeViewSet, basename='recipes'),

urlpatterns = [
    path('', include('users.urls')),
    path('', include(router.urls)),
]
