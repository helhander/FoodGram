from rest_framework.routers import DefaultRouter


class NoPUTRouter(DefaultRouter):
    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)
        bound_methods.pop('put', None)
        return bound_methods
