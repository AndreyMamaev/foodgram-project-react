from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .mixins import RetrieveListViewSet
from .serializers import (
    FavoriteSerializer, IngredientsSerializer, TagsSerializer,
    RecipesSerializer, CartSerializer
)
from .permissions import IsAuthorOrReadOnly
from .filters import RecipeFilter
from recipes.models import (
    Ingredient, Tag, Recipe,
    Favorite, Cart, IngredientRecipe
)
from .utils import ingredients_to_txt


class IngredientsViewSet(RetrieveListViewSet):
    """Вьюсет ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = None


class TagsViewSet(RetrieveListViewSet):
    """Вьюсет тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    lookup_field = 'name'


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""
    queryset = Recipe.objects.all()
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    serializer_class = RecipesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @action(detail=True, methods=['POST',])
    def favorite(self, request, pk):
        favorite_recipe = get_object_or_404(Recipe, id=pk)
        data = {'favorite_recipe': pk, 'user': request.user.id}
        serializer = FavoriteSerializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            Favorite.objects.create(favorite_recipe=favorite_recipe, user=request.user)
        return Response(self.get_serializer(favorite_recipe).data)
    
    @favorite.mapping.delete
    def favorite_delete(self, request, pk):
        favorite_recipe = get_object_or_404(Recipe, id=pk)
        data = {'favorite_recipe': pk, 'user': request.user.id}
        serializer = FavoriteSerializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            get_object_or_404(
                Favorite, favorite_recipe=favorite_recipe, user=request.user
            ).delete()
        return Response(self.get_serializer(favorite_recipe).data)
    
    @action(detail=True, methods=['POST',])
    def shopping_cart(self, request, pk):
        added_to_cart_recipe = get_object_or_404(Recipe, id=pk)
        data = {'added_to_cart_recipe': pk, 'user': request.user.id}
        serializer = CartSerializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            Cart.objects.create(added_to_cart_recipe=added_to_cart_recipe, user=request.user)
        return Response(self.get_serializer(added_to_cart_recipe).data)
    
    @shopping_cart.mapping.delete
    def shopping_cart_delete(self, request, pk):
        added_to_cart_recipe = get_object_or_404(Recipe, id=pk)
        data = {'added_to_cart_recipe': pk, 'user': request.user.id}
        serializer = CartSerializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            get_object_or_404(Cart, added_to_cart_recipe=added_to_cart_recipe, user=request.user).delete()
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
