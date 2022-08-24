from rest_framework import serializers,status
from django.shortcuts import get_object_or_404

from core.serializers import Base64FileField
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient, ShoppingCart
from django.contrib.auth import get_user_model
from users.models import Subscription
from djoser.serializers import UserCreateSerializer, UserSerializer


User = get_user_model()
USER_BASE_FIELDS = ('email', 'id', 'username', 'first_name', 'last_name')


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = USER_BASE_FIELDS

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request_user = self.context['request'].user
        data['is_subscribed'] = instance.subscribers.filter(
            subscriber=request_user
        ).exists()
        return data


class CustomUserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


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
    is_favorited = serializers.BooleanField(read_only=True)
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = TagSerializer(instance.tags, many=True).data
        data['ingredients'] = RecipeIngredientRepSerializer(
            instance.recipe_ingredients, many=True
        ).data
        request_user = self.context['request'].user
        data['is_favorited'] = request_user.favorites.filter(
            recipes=instance
        ).exists()
        data['is_in_shopping_cart'] = request_user.shopping_cart.filter(
            recipes=instance
        ).exists()
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


class ShoppingCartSerializer(serializers.ModelSerializer):
    cooking_time = serializers.IntegerField(
        source='cooking_time_min', read_only=True
    )
    name = serializers.CharField(read_only=True)
    image = serializers.CharField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
