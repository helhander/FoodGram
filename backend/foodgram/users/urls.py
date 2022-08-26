from core.urls import NoPUTRouter

from .views import CustomUserViewSet
from django.urls import include, path

app_name = 'users'


router = NoPUTRouter()

router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
