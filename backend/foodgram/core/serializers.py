import base64

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.text import slugify
from rest_framework import serializers

from foodgram.settings import MEDIA_URL
from recipes.models import Recipe, RecipeIngredient


class Base64FileField(serializers.Field):
    def to_representation(self, value):
        return f'{MEDIA_URL}{value}'

    def to_internal_value(self, data):
        try:
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = slugify(self.context['request'].data['name'], True)
            file = ContentFile(base64.b64decode(imgstr))
            return default_storage.save(f'{file_name}.{ext}', file)
        except Exception:
            raise ValueError('Wrong image value')


class RecipeSimpleSerializer(serializers.ModelSerializer):
    cooking_time = serializers.IntegerField(
        source='cooking_time_min', read_only=True
    )
    name = serializers.CharField(read_only=True)
    image = serializers.CharField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


def modify_recipe_tags_and_ingredients(recipe, tags, ingredients_data):
    recipe.tags.set(tags)

    RecipeIngredient.objects.filter(
        recipe=recipe,
    ).delete()
    recipe_ingredients = []
    ingredients = []
    for ingredient_data in ingredients_data:
        ingredient = ingredient_data.get('ingredient')
        recipe_ingredient = RecipeIngredient(
            ingredient=ingredient,
            amount=ingredient_data.get('amount'),
            recipe=recipe,
        )
        recipe_ingredients.append(recipe_ingredient)
        ingredients.append(ingredient)
    RecipeIngredient.objects.bulk_create(recipe_ingredients)
    recipe.ingredients.set(ingredients)
    return recipe
