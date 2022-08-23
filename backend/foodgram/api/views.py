from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    DownloadShoppingCartSerializer,
    ShoppingCartSerializer
)
from core.views import ListRetrieveViewSet
from recipes.models import Tag, Ingredient, Recipe, ShopingCart
from rest_framework import filters, status, viewsets
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import ReadOnly, IsMeAndSuperUserAndAdmin


User = get_user_model()

# class CustomUserViewSet(UserViewSet):
#     def get_object(self):
#         if self.kwargs.get('username') == 'me':
#             username = self.request.user
#         else:
#             username = self.kwargs.get('username')
#         self.check_object_permissions(self.request, obj)
#         return obj
class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(detail=True,methods=['delete'], url_path='shopping_cart')
    def remove_user_cart_recipe(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        user.shoping_cart.get().recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,methods=['post'], url_path='shopping_cart')
    def add_user_cart_recipe(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        shoping_cart = ShopingCart.objects.get_or_create(user=user)
        shoping_cart[0].recipes.add(recipe)
        serializer = ShoppingCartSerializer(recipe)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)

class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ShoppingCartSerializer

    def get_permissions(self):
        return [permission() for permission in [IsMeAndSuperUserAndAdmin]]
        if self.action == 'list':
            return [IsMeAndSuperUserAndAdmin]
        else:
            return [IsMeAndSuperUserAndAdmin]

    def get_queryset(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        return recipe
#,permission_classes=(IsMeAndSuperUserAndAdmin,)


class DownloadShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = DownloadShoppingCartSerializer
    # def perform_create(self, serializer):        
    #     serializer.save(author=self.request.user)
