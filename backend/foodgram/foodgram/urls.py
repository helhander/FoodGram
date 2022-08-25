from django.urls import include, path
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('api/', include('djoser.urls')),    
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('users.urls')),
    path('api/', include('api.urls'), name='api'),
    path('admin/', admin.site.urls),
]
