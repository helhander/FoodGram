from django.contrib import admin
from .models import Subscription

from django.contrib.auth import get_user_model

User = get_user_model()


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'subscriber')


admin.site.register(Subscription, SubscriptionAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
