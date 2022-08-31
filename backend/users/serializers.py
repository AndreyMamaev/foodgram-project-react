from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from users.models import User, Follow
from recipes.models import Recipe


class RecipeFollowSerializer(serializers.ModelSerializer):
    """Сериалайзер рецептов для страницы подписок."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователей."""
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
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class FollowUserSerializer(UserSerializer):
    """Сериалайзер пользователей в подписках."""
    recipes = RecipeFollowSerializer(many=True, read_only=True)
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


class FollowSerializer(UserSerializer):
    """Сериалайзер подписок."""

    class Meta:
        model = Follow
        fields = (
            'user',
            'author'
        )
    

    def validate(self, data):
        author = data.get('author')
        user = data.get('user')
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        exist = Follow.objects.filter(author=author, user=user).exists()
        request = self.context.get('request')
        if request.method == 'POST' and exist:
            raise serializers.ValidationError(
                'Вы уже подписаны на автора!'
            )
        if request.method == 'DELETE' and not exist:
            raise serializers.ValidationError(
                'Вы не подписаны на автора!'
                )
        return data
