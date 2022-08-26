from rest_framework import serializers

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from api.serializers import RecipeSimpleSerializer

User = get_user_model()
USER_BASE_FIELDS = ('email', 'id', 'username', 'first_name', 'last_name')


class SubscribeSerializer(serializers.ModelSerializer):    
    recipes = RecipeSimpleSerializer(many=True, required=False)
    recipes_count = serializers.IntegerField(required=False)
    is_subscribed = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = (
            *USER_BASE_FIELDS,'recipes','recipes_count','is_subscribed'
        )
    def to_representation(self, instance):
        user = self.context['request'].user
        data = super().to_representation(instance)
        recipes = RecipeSimpleSerializer(data=instance.recipes.all(),many=True)
        recipes.is_valid()
        data['recipes'] = recipes.data
        data['recipes_count'] = instance.recipes.count()
        data['is_subscribed'] = user.subscribing.filter(subscriber=user).exists()
        return data        
