# -*- coding: utf-8 -*-

from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


# class UserAccountTypeServiceInline(admin.TabularInline):
#     model = User.accounts_types_services.through
#     extra = 0

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password')
        }),
        (_('User info'), {
            'fields': (
                'address', 'birthday', 'country_code', 'country_name', 'gender', 'language', 'mobile_phone',
                'image_url', 'initials_bg_color'
            ),
        }),
        (_('Added fields'), {
            'fields': ('email_is_validated', 'is_deleted', 'mobile_phone_is_valid', 'mobile_phone_is_validated'),
        }),
    )
    list_display = (
        '__str__', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_deleted',
        'last_update_at', 'last_update_by'
    )
    list_filter = ('email_is_validated', 'gender', 'is_active', 'is_deleted', 'is_staff', 'mobile_phone_is_valid', 'mobile_phone_is_validated', 'language')
    search_fields = ('country_name', 'email', 'first_name', 'last_name', 'mobile_phone', 'username')

    def save_model(self, request, obj, form, change):
        if request.user:
            obj.created_by = request.user
            obj.last_update_by = request.user
        obj.last_update_at = datetime.datetime.now()
        super().save_model(request, obj, form, change)


    # inlines = [
    #     UserAccountTypeServiceInline,
    # ]

    # def get_queryset(self, request):
    #     # prefetch accounts types services
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.prefetch_related('accounts_types_services')
    #     return queryset


class UserEmailConfirmationKeyAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('key', 'user')
        }),
    )
    list_display = ('__str__', 'key', 'user')
    list_filter = ('user', )
    search_fields = ('key', 'user__username')


admin.site.register(User, UserAdmin)
admin.site.register(UserEmailConfirmationKey, UserEmailConfirmationKeyAdmin)



