from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models import Ingredient, Tag, Recipe, IngredientRecipe, Favorite, Cart, TagRecipe
from users.serializers import UserSerializer

class IngredientsSerializer(serializers.ModelSerializer):
    '''Сериалайзер ингредиентов.'''
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

class IngredientsRecipeSerializer(serializers.ModelSerializer):
    '''Сериалайзер ингредиентов рецепта.'''
    id = serializers.PrimaryKeyRelatedField(source='ingredient.id', read_only='True')
    name = serializers.StringRelatedField(source='ingredient.name', read_only='True')
    measurement_unit = serializers.StringRelatedField(source='ingredient.measurement_unit', read_only='True')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

class TagsSerializer(serializers.ModelSerializer):
    '''Сериалайзер тэгов.'''
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

class RecipesSerializer(serializers.ModelSerializer):
    '''Сериалайзер рецептов.'''
    author = UserSerializer(many=False, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
    
    def get_ingredients(self, obj):
        ingredients =  IngredientRecipe.objects.filter(recipe=obj)
        serializer = IngredientsRecipeSerializer(ingredients, many=True)
        return serializer.data
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, favorite_recipe=obj).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Cart.objects.filter(user=request.user, added_to_cart_recipe=obj).exists()
    
    def create(self, validated_data):
        request = self.context.get('request')
        author=request.user
        tags_id = self.initial_data.get('tags')
        ingredients_id = self.initial_data.get('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        for tag_id in tags_id:
            if Tag.objects.filter(id=tag_id).exists():
                TagRecipe.objects.create(recipe=recipe, tag_id=tag_id)
            else:
                raise serializers.ValidationError(
                "Тэга не существует!"
                )
        for ingredient_id in ingredients_id:
            if Ingredient.objects.filter(id=ingredient_id.get('id')).exists():
                IngredientRecipe.objects.create(
                    recipe=recipe,
                    ingredient_id=ingredient_id.get('id'),
                    amount=ingredient_id.get('amount')
                )
            else:
                raise serializers.ValidationError(
                "Ингредиента не существует!"
                )
        return recipe

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if instance.author != request.user:
            raise serializers.ValidationError(
                "Обновление рецепта доступно только автору рецепта!"
                )
        tags_id = self.initial_data.get('tags')
        ingredients_id = self.initial_data.get('ingredients')
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        for tag_id in tags_id:
            if Tag.objects.filter(id=tag_id).exists():
                TagRecipe.objects.create(recipe=instance, tag_id=tag_id)
            else:
                raise serializers.ValidationError(
                "Тэга не существует!"
                )
        for ingredient_id in ingredients_id:
            if Ingredient.objects.filter(id=ingredient_id.get('id')).exists():
                IngredientRecipe.objects.create(
                    recipe=instance,
                    ingredient_id=ingredient_id.get('id'),
                    amount=ingredient_id.get('amount')
                )
            else:
                raise serializers.ValidationError(
                "Ингредиента не существует!"
                )
        return instance
    
    

    