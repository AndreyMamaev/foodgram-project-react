from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404

from .models import User, Follow
from .serializers import UserSerializer, FollowSerializer

    
class UsersViewSet(UserViewSet):
    '''Вьюсет пользователей.'''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'subscriptions' or self.action == 'subscribe':
            return FollowSerializer
        return UserSerializer
    
    @action(detail=False)
    def subscriptions(self, request):
        user = request.user
        following = User.objects.filter(following__user=user)
        return Response(self.get_serializer(following, many=True).data)
    
    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.user == author:
            raise serializers.ValidationError(
                    "Нельзя подписаться на самого себя!"
                    )
        exist = Follow.objects.filter(author=author, user=request.user).exists()
        if request.method == 'POST':
            if exist:
                raise serializers.ValidationError(
                    "Вы уже подписаны на автора!"
                    )
            Follow.objects.create(author=author, user=request.user)
        elif request.method == 'DELETE':
            if not exist:
                raise serializers.ValidationError(
                    "Вы не подписаны на автора!"
                    )
            Follow.objects.get(author=author, user=request.user).delete()
        return Response(self.get_serializer(author).data)
