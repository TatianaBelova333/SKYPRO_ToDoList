from django.contrib import admin
from core.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': (
            "username",
            "password",
            'first_name',
            'last_name',
            'email',
            "is_active",
            "is_staff",
            'last_login',
            'date_joined',
        )}),
    )

