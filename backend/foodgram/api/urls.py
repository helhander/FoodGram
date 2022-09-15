from django.urls import include, path

from core.urls import NoPUTRouter
from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'api'


router_v1 = NoPUTRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingrediants')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
]
