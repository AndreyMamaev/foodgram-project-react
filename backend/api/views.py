from django.http import HttpResponse
from rest_framework import viewsets, serializers, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .mixins import RetrieveListViewSet
from .serializers import IngredientsSerializer, TagsSerializer, RecipesSerializer
from .permissions import IsAuthorOrReadOnly
from .filters import RecipeFilter
from recipes.models import Ingredient, Tag, Recipe, Favorite, Cart, IngredientRecipe


class IngredientsViewSet(RetrieveListViewSet):
    '''Вьюсет жанров.'''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = None

class TagsViewSet(RetrieveListViewSet):
    '''Вьюсет жанров.'''
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    lookup_field = 'name'

class RecipesViewSet(viewsets.ModelViewSet):
    '''Вьюсет жанров.'''
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
    serializer_class = RecipesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk):
        recipe = Recipe.objects.get(id=pk)
        exist = Favorite.objects.filter(favorite_recipe=recipe, user=request.user).exists()
        if request.method == 'POST':
            if exist:
                raise serializers.ValidationError(
                    "Рецепт уже в избранном!"
                    )
            Favorite.objects.create(favorite_recipe=recipe, user=request.user)
        elif request.method == 'DELETE':
            if not exist:
                raise serializers.ValidationError(
                    "Рецепт не в избранном!"
                    )
            Favorite.objects.get(favorite_recipe=recipe, user=request.user).delete()
        return Response(self.get_serializer(recipe).data)
    
    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk):
        recipe = Recipe.objects.get(id=pk)
        exist = Cart.objects.filter(added_to_cart_recipe=recipe, user=request.user).exists()
        if request.method == 'POST':
            if exist:
                raise serializers.ValidationError(
                    "Рецепт уже в корзине!"
                    )
            Cart.objects.create(added_to_cart_recipe=recipe, user=request.user)
        elif request.method == 'DELETE':
            if not exist:
                raise serializers.ValidationError(
                    "Рецепт не в корзине!"
                    )
            Cart.objects.get(added_to_cart_recipe=recipe, user=request.user).delete()
        return Response(self.get_serializer(recipe).data)
    
    @action(detail=False,)
    def download_shopping_cart(self, request):
        spisok = {}
        carts = Cart.objects.filter(user=request.user)
        for cart in carts:
            recipe = cart.added_to_cart_recipe
            ingredients = recipe.ingredients.all()
            for ingredient in ingredients:
                l = IngredientRecipe.objects.get(recipe=recipe, ingredient=ingredient)
                name = l.ingredient.name + ' (' + l.ingredient.measurement_unit + ')'
                if name not in spisok:
                    spisok[name] = l.amount
                else:
                    spisok[name] += l.amount
        content = ''
        for key in spisok:
            content += key + ' - ' + str(spisok[key]) + '\n'
        return HttpResponse(content, content_type='text/plain')
