from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCart,
    Tag,
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_number')
    search_fields = ('name', 'author__username', 'tags__slug')

    def favorite_number(self, recipe):
        return recipe.favorites.count()


admin.site.register(Recipe, RecipeAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


admin.site.register(Tag, TagAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


admin.site.register(Ingredient, IngredientAdmin)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


admin.site.register(RecipeIngredient, RecipeIngredientAdmin)


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'tag')


admin.site.register(RecipeTag, RecipeTagAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Favorite, FavoriteAdmin)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(ShoppingCart, ShoppingCartAdmin)
