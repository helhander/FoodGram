from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import FileResponse
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    ShoppingCartSerializer
)
from core.views import ListRetrieveViewSet,get_shopping_cart_file
from recipes.models import Tag, Ingredient, Recipe, ShoppingCart
from rest_framework import filters, status, viewsets
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import ReadOnly, IsMeAndSuperUserAndAdmin

SHOPPING_CART_FILENAME = 'Список покупок'
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

    @action(detail=True,methods=['post','delete'], url_path='shopping_cart')
    def add_shopping_cart_recipe(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user        
        shopping_cart = ShoppingCart.objects.get_or_create(user=user)[0]
        if request.method=='DELETE':
            shopping_cart.recipes.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)

        shopping_cart.recipes.add(recipe)
        serializer = ShoppingCartSerializer(recipe)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)


    @action(detail=False,methods=['get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        file = get_shopping_cart_file(self, request)
        return FileResponse(file, as_attachment=True, filename=SHOPPING_CART_FILENAME)



    # def perform_create(self, serializer):        
    #     serializer.save(author=self.request.user)
