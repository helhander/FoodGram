from django.shortcuts import render
from django.contrib.auth import get_user_model
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
)
from core.views import ListRetrieveViewSet
from recipes.models import Tag, Ingredient, Recipe
from rest_framework import filters, status, viewsets

from .permissions import ReadOnly

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (ReadOnly,)


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    # def perform_create(self, serializer):        
    #     serializer.save(author=self.request.user)
