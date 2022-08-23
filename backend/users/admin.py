from django.contrib import admin

from .models import User, Follow

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'password') 
    search_fields = ('username', 'email', 'first_name', 'last_name',) 
    list_filter = ('date_joined',) 

admin.site.register(User, UserAdmin,) 
admin.site.register(Follow)
