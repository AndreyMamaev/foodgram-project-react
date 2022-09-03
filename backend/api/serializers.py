from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag, TagRecipe)
from rest_framework import serializers
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер ингредиентов рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id', read_only='True'
    )
    name = serializers.StringRelatedField(
        source='ingredient.name', read_only='True'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit', read_only='True'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер тэгов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер рецептов."""
    author = CustomUserSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        serializer = IngredientRecipeSerializer(ingredients, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, favorite_recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Cart.objects.filter(
            user=request.user, added_to_cart_recipe=obj
        ).exists()

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        validated_data['author'] = author
        tags_id = self.initial_data.get('tags')
        ingredients_id = self.initial_data.get('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        tags = [
            TagRecipe(
                recipe=recipe,
                tag_id=tag_id
            ) for tag_id in tags_id
        ]
        TagRecipe.objects.bulk_create(tags)
        ingredients = [
            IngredientRecipe(
                recipe=recipe,
                ingredient_id=ingredient_id.get('id'),
                amount=ingredient_id.get('amount')
            ) for ingredient_id in ingredients_id
        ]
        IngredientRecipe.objects.bulk_create(ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags_id = self.initial_data.get('tags')
        ingredients_id = self.initial_data.get('ingredients')
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        tags = [
            TagRecipe(
                recipe=instance,
                tag_id=tag_id
            ) for tag_id in tags_id
        ]
        TagRecipe.objects.bulk_create(tags)
        ingredients = [
            IngredientRecipe(
                recipe=instance,
                ingredient_id=ingredient_id.get('id'),
                amount=ingredient_id.get('amount')
            ) for ingredient_id in ingredients_id
        ]
        IngredientRecipe.objects.bulk_create(ingredients)
        return super().update(instance, validated_data)

    def validate(self, data):
        tags_id = self.initial_data.get('tags')
        ingredients_id = self.initial_data.get('ingredients')
        for tag_id in tags_id:
            if not Tag.objects.filter(id=tag_id).exists():
                raise serializers.ValidationError(
                    'Тэга не существует!'
                )
        for ingredient_id in ingredients_id:
            if not Ingredient.objects.filter(
                id=ingredient_id.get('id')
            ).exists():
                raise serializers.ValidationError(
                    'Ингредиента не существует!'
                )
        return data


class FavoriteSerializer(CustomUserSerializer):
    """Сериалайзер избранного."""

    class Meta:
        model = Favorite
        fields = (
            'user',
            'favorite_recipe'
        )

    def validate(self, data):
        favorite_recipe = data.get('favorite_recipe')
        user = data.get('user')
        exist = Favorite.objects.filter(
            favorite_recipe=favorite_recipe, user=user
        ).exists()
        request = self.context.get('request')
        if request.method == 'POST' and exist:
            raise serializers.ValidationError(
                'Рецепт уже в избранном!'
            )
        if request.method == 'DELETE' and not exist:
            raise serializers.ValidationError(
                'Рецепт не в избранном!'
                )
        return data


class CartSerializer(CustomUserSerializer):
    """Сериалайзер корзины."""

    class Meta:
        model = Cart
        fields = (
            'user',
            'added_to_cart_recipe'
        )

    def validate(self, data):
        added_to_cart_recipe = data.get('added_to_cart_recipe')
        user = data.get('user')
        exist = Cart.objects.filter(
            added_to_cart_recipe=added_to_cart_recipe, user=user
        ).exists()
        request = self.context.get('request')
        if request.method == 'POST' and exist:
            raise serializers.ValidationError(
                'Рецепт уже в корзине!'
            )
        if request.method == 'DELETE' and not exist:
            raise serializers.ValidationError(
                'Рецепт не в корзине!'
                )
        return data
