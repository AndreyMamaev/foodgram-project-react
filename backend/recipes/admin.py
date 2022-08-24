from django.contrib import admin

from .models import IngredientRecipe, Recipe, Ingredient, Tag, TagRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites',) 
    search_fields = ('name', 'author', 'tags',) 
    list_filter = ('name', 'author', 'tags','pub_date',)
    readonly_fields = ('count_favorites',)

    def count_favorites(self, obj):
        return obj.favorite_recipe.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',) 
    search_fields = ('name',) 
    list_filter = ('name',)


admin.site.register(Tag) 
admin.site.register(TagRecipe) 
admin.site.register(IngredientRecipe) 
