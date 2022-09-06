import base64

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.text import slugify
from rest_framework import serializers

from recipes.models import Recipe


class Base64FileField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = slugify(self.context['request'].data['name'], True)
            file = ContentFile(base64.b64decode(imgstr))
            return default_storage.save(f'{file_name}.{ext}', file)
        except Exception:
            raise serializers.ValidationError('Ошибка')


class IngredientField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = slugify(self.context['request'].data['name'], True)
            file = ContentFile(base64.b64decode(imgstr))
            file_url = default_storage.save(f'{file_name}.{ext}', file)
        except Exception:
            raise serializers.ValidationError('Ошибка')

        return file_url


class RecipeSimpleSerializer(serializers.ModelSerializer):
    cooking_time = serializers.IntegerField(
        source='cooking_time_min', read_only=True
    )
    name = serializers.CharField(read_only=True)
    image = serializers.CharField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
