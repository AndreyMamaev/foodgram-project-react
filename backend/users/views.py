from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, User
from .serializers import (CustomUserSerializer, FollowSerializer,
                          FollowUserSerializer)


class CustomUserViewSet(UserViewSet):
    """Вьюсет пользователей."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False)
    def subscriptions(self, request):
        user = request.user
        following = User.objects.filter(following__user=user)
        following_paginate = self.paginate_queryset(following)
        return self.get_paginated_response(FollowUserSerializer(
            following_paginate,
            many=True,
            context={'request': request}
        ).data)

    @action(detail=True, methods=['POST', ])
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        data = {'author': id, 'user': request.user.id}
        serializer = FollowSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        Follow.objects.create(author=author, user=request.user)
        return Response(FollowUserSerializer(
            author, context={'request': request}
        ).data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        data = {'author': id, 'user': request.user.id}
        serializer = FollowSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        get_object_or_404(Follow, author=author, user=request.user).delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
