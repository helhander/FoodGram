from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import AllowAllExceptListAction
from .models import Subscription
from .serializers import SubscribeSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    permission_classes = (AllowAllExceptListAction,)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe')
    def subscribe_actions(self, request, id):
        author = get_object_or_404(User, pk=id)
        subscriber = request.user
        subscription = Subscription.objects.get_or_create(
            author=author, subscriber=subscriber
        )
        if request.method == 'DELETE':
            subscription[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = SubscribeSerializer(author, context={'request': request})
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

    @action(detail=False, methods=['get'], url_path='subscriptions')
    def get_subsriptions(self, request):
        subscriptions = User.objects.filter(
            subscribers__subscriber=request.user
        ).order_by('-id')
        recipes_limit = request.query_params.get('recipes_limit')
        recipes_limit_number = None
        if recipes_limit is not None:
            try:
                recipes_limit_number = int(recipes_limit)
            except ValueError:
                raise ValueError(
                    f'Параметр recipes_limit {recipes_limit}'
                    ' - должнен быть числом'
                )
        page = self.paginate_queryset(subscriptions)
        serializer = SubscribeSerializer(
            page,
            many=True,
            context={
                'request': request,
                'recipes_limit_number': recipes_limit_number,
            },
        )
        return self.get_paginated_response(serializer.data)
