from django.contrib.auth.hashers import make_password
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from rest_framework import serializers
from users.models import Follow, User


class RecipeFollowSerializer(serializers.ModelSerializer):
    """Сериалайзер рецептов для страницы подписок."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserSerializer(UserSerializer):
    """Сериалайзер пользователей."""
    is_subsсribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subsсribed', 'password'
        )
        lookup_field = ('username',)
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
            'email': {'required': True}
        }

    def get_is_subsсribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password')
        )
        return super(CustomUserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class FollowUserSerializer(CustomUserSerializer):
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


class FollowSerializer(CustomUserSerializer):
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
