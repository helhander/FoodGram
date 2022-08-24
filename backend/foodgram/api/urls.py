from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeViewSet,
    TagViewSet,
    IngredientViewSet,
    # CustomUserViewSet
)

app_name = 'api'
API_VERSION_V1 = 'v1'

class NoPUTRouter(DefaultRouter):
    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)
        bound_methods.pop('put', None)
        return bound_methods


router_v1 = NoPUTRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingrediants')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
# router_v1.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path(f'{API_VERSION_V1}/', include(router_v1.urls)),
]
