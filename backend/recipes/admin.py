from django.contrib import admin

from .models import IngredientRecipe, Recipe, Ingredient, Tag, TagRecipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',) 
    search_fields = ('name', 'author', 'tags',) 
    list_filter = ('pub_date',)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',) 
    search_fields = ('name',) 

admin.site.register(Recipe, RecipeAdmin,) 
admin.site.register(Ingredient, IngredientAdmin,) 
admin.site.register(Tag) 
admin.site.register(TagRecipe) 
admin.site.register(IngredientRecipe) 
