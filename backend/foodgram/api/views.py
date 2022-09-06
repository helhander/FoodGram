from django.contrib.auth import get_user_model
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action

from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from core.views import (
    IngredientSearchFilter,
    ListRetrieveNoPagViewSet,
    RecipeFilter,
    get_recipe_action_response,
    get_shopping_cart_file,
)
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag

from .permissions import ReadOnly, ReadOnlyOrAuthorOrAdmin

SHOPPING_CART_FILENAME = 'Список покупок'
User = get_user_model()


class TagViewSet(ListRetrieveNoPagViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (ReadOnly,)
    lookup_field = 'slug'


class IngredientViewSet(ListRetrieveNoPagViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    permission_classes = (ReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (ReadOnlyOrAuthorOrAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

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
