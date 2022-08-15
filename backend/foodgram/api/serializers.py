from rest_framework import serializers
from core.serializers import Base64FileField
from recipes.models import Tag, Ingredient, Recipe,RecipeIngredient
from django.contrib.auth import get_user_model
from users.models import Subscription

User = get_user_model()
class TestUserSerializer(serializers.ModelSerializer):
    username=serializers.IntegerField(source='username',read_only=True)
    class Meta:
        model = User
        fields = ('username')
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name','last_name')

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
    id = serializers.PrimaryKeyRelatedField(source='ingredient',queryset=Ingredient.objects.all(), required=False)
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount','recipe')


class RecipeSerializer(serializers.ModelSerializer):
    cooking_time = serializers.IntegerField(source='cooking_time_min')
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)#read_only=True и прокидывать значение аналогично предыдущему проекту
    author = UserSerializer(default=serializers.CurrentUserDefault(),read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, required=False)
    image = Base64FileField()
    class Meta:
        model = Recipe
        fields = ('id', 'tags','author','ingredients','name', 'image', 'text', 'cooking_time')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = TagSerializer(instance.tags, many=True).data
        # data['ingredients'] = IngredientSerializer(instance.ingredients, many=True).data
        return data
    
    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe_ingredients = []
        for ingredient in ingredients:
            recipe_ingredient = RecipeIngredient.objects.create(
                ingredient = ingredient.get('ingredient'),
                amount = ingredient.get('amount'),
                recipe = recipe
            )
            recipe_ingredients.append(ingredient.get('ingredient'))
        recipe.ingredients.set(recipe_ingredients)
        return recipe
        return super().create(validated_data)


    #     return UserProfile.objects.create_user(**validated_data)

