
from django.contrib.auth import get_user_model
from django.http import FileResponse
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
)
from core.views import get_recipe_action_response

from core.views import ListRetrieveNoPagViewSet, get_shopping_cart_file
from recipes.models import Tag, Ingredient, Recipe, ShoppingCart, Favorite
from rest_framework import filters, status, viewsets
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import ReadOnly, IsMeAndSuperUserAndAdmin, IsAdmin

SHOPPING_CART_FILENAME = 'Список покупок'
User = get_user_model()


class TagViewSet(ListRetrieveNoPagViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveNoPagViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = ((IsAdmin | ReadOnly),)
    @action(detail=True, methods=['post', 'delete'], url_path='favorite')
    def favorite_actions(self, request, pk):
        response = get_recipe_action_response(self, request, pk, Favorite)
        return response

    @action(detail=True, methods=['post', 'delete'], url_path='shopping_cart')
    def shopping_cart_actions(self, request, pk):
        response = get_recipe_action_response(self, request, pk, ShoppingCart)
        return response

    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        file = get_shopping_cart_file(self, request)
        return FileResponse(
            file, as_attachment=True, filename=SHOPPING_CART_FILENAME
        )
