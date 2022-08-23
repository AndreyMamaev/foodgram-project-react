from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from users.models import User, Follow
from recipes.models import Recipe


class RecipesFollowSerializer(serializers.ModelSerializer):
    '''Сериалайзер рецептов для страницы подписок.'''
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

class UserSerializer(serializers.ModelSerializer):
    '''Сериалайзер пользователей.'''
    is_subsсribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'is_subsсribed'
        )
        lookup_field = ('username',)
        extra_kwargs = {
            'password': {'required': False},
            'email': {'required': True}
        }

    def get_is_subsсribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()

class FollowSerializer(UserSerializer):
    '''Сериалайзер подписок.'''
    recipes = RecipesFollowSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subsсribed', 'recipes', 'recipes_count'
        )
        lookup_field = ('username',)
        extra_kwargs = {
            'password': {'required': False},
            'email': {'required': True}
        }
    
    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
        

