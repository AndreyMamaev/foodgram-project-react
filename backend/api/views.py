from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipeFilter
from .mixins import RetrieveListViewSet
from .permissions import IsAuthorOrReadOnly
from .serializers import (CartSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          TagSerializer)
from .utils import ingredients_to_txt


class IngredientViewSet(RetrieveListViewSet):
    """Вьюсет ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = None


class TagViewSet(RetrieveListViewSet):
    """Вьюсет тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    lookup_field = 'name'


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""
    queryset = Recipe.objects.all()
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @action(detail=True, methods=['POST', ])
    def favorite(self, request, pk):
        favorite_recipe = get_object_or_404(Recipe, id=pk)
        data = {'favorite_recipe': pk, 'user': request.user.id}
        serializer = FavoriteSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        Favorite.objects.create(
            favorite_recipe=favorite_recipe,
            user=request.user
        )
        return Response(self.get_serializer(favorite_recipe).data)

    @favorite.mapping.delete
    def unfavorite(self, request, pk):
        favorite_recipe = get_object_or_404(Recipe, id=pk)
        data = {'favorite_recipe': pk, 'user': request.user.id}
        serializer = FavoriteSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        get_object_or_404(
            Favorite,
            favorite_recipe=favorite_recipe,
            user=request.user
        ).delete()
        return Response(self.get_serializer(favorite_recipe).data)

    @action(
        detail=True, methods=['POST', ],
        url_path='shopping_cart'
    )
    def add_to_shopping_cart(self, request, pk):
        added_to_cart_recipe = get_object_or_404(Recipe, id=pk)
        data = {'added_to_cart_recipe': pk, 'user': request.user.id}
        serializer = CartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        Cart.objects.create(
            added_to_cart_recipe=added_to_cart_recipe,
            user=request.user
        )
        return Response(self.get_serializer(added_to_cart_recipe).data)

    @add_to_shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        added_to_cart_recipe = get_object_or_404(Recipe, id=pk)
        data = {'added_to_cart_recipe': pk, 'user': request.user.id}
        serializer = CartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        get_object_or_404(
            Cart,
            added_to_cart_recipe=added_to_cart_recipe,
            user=request.user
        ).delete()
        return Response(self.get_serializer(added_to_cart_recipe).data)

    @action(detail=False,)
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__added_to_cart_recipe__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(sum=Sum('amount'))
        shopping_list = ingredients_to_txt(ingredients)
        return HttpResponse(shopping_list, content_type='text/plain')
