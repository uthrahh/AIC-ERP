from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'startup', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('AIC-CIIC Profile', {'fields': ('role', 'startup', 'phone', 'last_login_at')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('AIC-CIIC Profile', {'fields': ('role', 'startup', 'phone')}),
    )
