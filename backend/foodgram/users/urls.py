from django.urls import include, path

from core.urls import NoPUTRouter

from .views import CustomUserViewSet

app_name = 'users'


router = NoPUTRouter()

router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
