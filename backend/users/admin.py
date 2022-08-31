from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name',
        'last_name', 'role', 'password'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('date_joined')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
