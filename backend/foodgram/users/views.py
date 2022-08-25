from rest_framework.decorators import action
from django.shortcuts import render
from djoser.views import UserViewSet

# Create your views here.
class SubscriberViewSet(UserViewSet):
    pass
    @action(detail=True, methods=['post', 'delete'], url_path='subscribe')
    def favorite_actions(self, request, id):
        # response = get_recipe_action_response(self, request, pk, Favorite)
        return True