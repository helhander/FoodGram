from django.urls import path

from .views import SubscriberViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
app_name = 'subscribes'

class NoPUTRouter(DefaultRouter):
    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)
        bound_methods.pop('put', None)
        return bound_methods


router_v1 = NoPUTRouter()

router_v1.register('users', SubscriberViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
]
# urlpatterns = [
#     path(
#         'users/',
#         SubscriberViewSet,
#         name='subscribes'
#     ),
# ]
