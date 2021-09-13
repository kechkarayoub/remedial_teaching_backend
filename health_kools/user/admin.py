# -*- coding: utf-8 -*-

from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _


class AccountTypeServiceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('type', 'service')
        }),
    )
    list_display = ('__str__', 'type_name', 'service_name')
    list_filter = ('type', 'service')
    search_fields = ('type', 'service')


class UserAccountTypeServiceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('account_type_service', 'user')
        }),
    )
    list_display = ('__str__', 'account_type_service', 'user')
    list_filter = ('account_type_service', 'user')
    search_fields = ('account_type_service__type', 'account_type_service__service', 'user__username')


class UserAccountTypeServiceInline(admin.TabularInline):
    model = User.accounts_types_services.through
    extra = 0


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            'fields': ('__str__', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password')
        }),
        (_('Added fields'), {
            'fields': ('email_is_valid', 'phone', 'phone_is_valid'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'email_is_valid', 'phone', 'phone_is_valid')
    list_filter = ('email_is_valid', 'is_active', 'is_staff', 'phone_is_valid')
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'username')
    inlines = [
        UserAccountTypeServiceInline,
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('accounts_types_services')
        return queryset


admin.site.register(User, UserAdmin)
admin.site.register(AccountTypeService, AccountTypeServiceAdmin)
admin.site.register(UserAccountTypeService, UserAccountTypeServiceAdmin)



