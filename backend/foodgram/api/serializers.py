from rest_framework import serializers
from users.serializers import CustomUserSerializer

from core.serializers import Base64FileField
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from django.contrib.auth import get_user_model
from users.models import Subscription


User = get_user_model()



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('subscriber', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe = serializers.ReadOnlyField()
    amount = serializers.IntegerField(required=False)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all(), required=False
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', 'recipe')


class RecipeIngredientRepSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    cooking_time = serializers.IntegerField(source='cooking_time_min')
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=False
    )
    author = CustomUserSerializer(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    ingredients = RecipeIngredientSerializer(many=True, required=False)
    image = Base64FileField()
    is_favorited = serializers.SerializerMethodField()#serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, recipe):
        request_user = self.context['request'].user
        is_favorited = request_user.favorites.filter(
            recipe=recipe
        ).exists() if not request_user.is_anonymous else False
        return is_favorited
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = TagSerializer(instance.tags, many=True).data
        data['ingredients'] = RecipeIngredientRepSerializer(
            instance.recipe_ingredients, many=True
        ).data
        request_user = self.context['request'].user
        data['is_in_shopping_cart'] = request_user.shopping_cart.filter(
            recipe=instance
        ).exists() if not request_user.is_anonymous else False
        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        recipe_ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        ingredients = []
        for recipe_ingredient in recipe_ingredients:
            RecipeIngredient.objects.create(
                ingredient=recipe_ingredient.get('ingredient'),
                amount=recipe_ingredient.get('amount'),
                recipe=recipe,
            )
            ingredients.append(recipe_ingredient.get('ingredient'))
        recipe.ingredients.set(ingredients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        if 'tags' in validated_data:
            tags = validated_data.get('tags')
            instance.tags.set(tags)
        if 'ingredients' in validated_data:
            RecipeIngredient.objects.filter(
                recipe=instance,
            ).delete()
            recipe_ingredients = validated_data.get('ingredients')
            ingredients = []
            for recipe_ingredient in recipe_ingredients:
                RecipeIngredient.objects.create(
                    ingredient=recipe_ingredient.get('ingredient'),
                    amount=recipe_ingredient.get('amount'),
                    recipe=instance,
                )
                ingredients.append(recipe_ingredient.get('ingredient'))
            instance.ingredients.set(ingredients)

        return instance


