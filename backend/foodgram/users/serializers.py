from rest_framework import serializers

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from core.serializers import RecipeSimpleSerializer

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
        ).exists() if not request_user.is_anonymous else False
        return data

class CustomUserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (*USER_BASE_FIELDS, 'password')

class SubscribeSerializer(CustomUserSerializer):    
    recipes = RecipeSimpleSerializer(many=True, required=False)
    recipes_count = serializers.IntegerField(required=False)
    class Meta:
        model = User
        fields = (
            *USER_BASE_FIELDS,'recipes','recipes_count'
        )
    def to_representation(self, instance):
        data = super().to_representation(instance)
        recipes = RecipeSimpleSerializer(data=instance.recipes.all(),many=True)
        recipes.is_valid()
        data['recipes'] = recipes.data
        data['recipes_count'] = instance.recipes.count()
        return data        
