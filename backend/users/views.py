from rest_framework.response import Response
from rest_framework.decorators import action
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404

from .models import User, Follow
from .serializers import UserSerializer, FollowSerializer, FollowUserSerializer

    
class UsersViewSet(UserViewSet):
    """Вьюсет пользователей."""
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
        return Response(FollowUserSerializer(following, many=True).data)
    
    @action(detail=True, methods=['POST',])
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        data = {'author': id, 'user': request.user.id}
        serializer = self.get_serializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            Follow.objects.create(author=author, user=request.user)
        return Response(FollowUserSerializer(author, context={'request': request}).data)

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id):
        author = get_object_or_404(User, id=id)
        data = {'author': id, 'user': request.user.id}
        serializer = FollowSerializer(
            data=data,
            context={'request': request}
        )
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            get_object_or_404(Follow, author=author, user=request.user).delete()
        return Response(FollowUserSerializer(author, context={'request': request}).data)
