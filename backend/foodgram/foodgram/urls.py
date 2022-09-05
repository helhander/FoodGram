from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('users.urls')),
    path('api/', include('api.urls'), name='api'),
    path('admin/', admin.site.urls),
]
