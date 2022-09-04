from rest_framework.decorators import action
from django.shortcuts import render
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import mixins, viewsets,status

from api.permissions import RetrieveOrMeActions
from .serializers import SubscribeSerializer
from django.db.models import Count

from .models import Subscription
User = get_user_model()
# Create your views here.
class CustomUserViewSet(UserViewSet):
    permission_classes = (RetrieveOrMeActions,)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe')
    def subscribe_actions(self, request, id):
        # response = get_recipe_action_response(self, request, pk, Favorite)
        author = get_object_or_404(User, pk=id)
        subscriber = request.user
        subscription = Subscription.objects.get_or_create(author=author, subscriber=subscriber)
        if request.method=='DELETE':
            subscription[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = SubscribeSerializer(author, context={'request': request})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)
    @action(detail=False, methods=['get'], url_path='subscriptions')
    def get_subsriptions(self, request):        
        subscriptions= User.objects.filter(subscribers__subscriber=request.user)
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            try:
                recipes_limit_number = int(recipes_limit)
                subscriptions= subscriptions.annotate(
                    total_recipes=Count('recipes')
                ).filter(total_recipes__lte=recipes_limit_number)
            except:
                raise ValueError(f'Value {recipes_limit} must be integer number')
        queryset = self.filter_queryset(subscriptions)        
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(page,many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
