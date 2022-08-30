from django.urls import include, path

from core.urls import NoPUTRouter

from .views import (
    RecipeViewSet,
    TagViewSet,
    IngredientViewSet,
)

app_name = 'api'
API_VERSION_V1 = 'v1'


router_v1 = NoPUTRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingrediants')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(f'{API_VERSION_V1}/', include(router_v1.urls)),
]
