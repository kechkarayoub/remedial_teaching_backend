# -*- coding: utf-8 -*-

from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


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
            'fields': ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password')
        }),
        (_('Added fields'), {
            'fields': ('country_code', 'country_name', 'email_is_validated', 'gender', 'phone', 'phone_is_valid', 'phone_is_validated', 'language'),
        }),
    )
    list_display = ('__str__', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'email_is_validated', 'phone', 'phone_is_validated')
    list_filter = ('email_is_validated', 'gender', 'is_active', 'is_staff', 'phone_is_valid', 'phone_is_validated', 'language')
    search_fields = ('country_name', 'email', 'first_name', 'last_name', 'phone', 'username')
    inlines = [
        UserAccountTypeServiceInline,
    ]

    def get_queryset(self, request):
        # prefetch accounts types services
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('accounts_types_services')
        return queryset


class UserEmailConfirmationKeyAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('key', 'user')
        }),
    )
    list_display = ('__str__', 'key', 'user')
    list_filter = ('user', )
    search_fields = ('key', 'user__username')


class UserSecurityQuestionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('response', 'security_question', 'user')
        }),
    )
    list_display = ('__str__', 'security_question', 'user')
    list_filter = ('user', )
    search_fields = ('response', 'security_question', 'user__username')


admin.site.register(User, UserAdmin)
admin.site.register(AccountTypeService, AccountTypeServiceAdmin)
admin.site.register(UserAccountTypeService, UserAccountTypeServiceAdmin)
admin.site.register(UserEmailConfirmationKey, UserEmailConfirmationKeyAdmin)
admin.site.register(UserSecurityQuestion, UserSecurityQuestionAdmin)



