# -*- coding: utf-8 -*-

from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


# class UserAccountTypeServiceInline(admin.TabularInline):
#     model = User.accounts_types_services.through
#     extra = 0


class EstablishmentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name', 'name_ar', 'type', 'address', 'address_ar', 'fax', 'is_active', 'is_deleted', 'logo_url',
                'phone', 'phone2', 'email', 'city'
            )
        }),
        (_('Added fields'), {
            'fields': (
                'fax_is_valid', 'fax_is_validated', 'mobile_phone', 'mobile_phone_is_valid', 'mobile_phone_is_validated',
                'phone_is_valid', 'phone_is_validated', 'phone2_is_valid', 'phone2_is_validated', 'website_url'
            ),
        }),
    )
    list_display = ('__str__', 'name', 'is_active', 'is_deleted', 'last_update_at')
    list_filter = (
        'is_active', 'is_deleted', 'type', 'city', 'mobile_phone_is_valid', 'mobile_phone_is_validated',
        'phone_is_valid', 'phone_is_validated', 'phone2_is_valid', 'phone2_is_validated',
    )
    search_fields = ('name', 'name_ar', 'address', 'address_ar', 'city')

    def save_model(self, request, obj, form, change):
        obj.last_update_at = datetime.datetime.now()
        super().save_model(request, obj, form, change)


class EstablishmentUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'account_type', 'establishment', 'is_active', 'is_deleted', 'user', 'is_accepted'
            )
        }),
        ("User info", {
            'fields': (
                'last_name', 'first_name', 'birthday', 'address', 'country_code', 'country_name', 'gender',
                'mobile_phone',
            )
        }),
        (_('Added fields'), {
            'fields': (
                'email_is_accepted', 'mobile_phone_is_accepted', 'mobile_phone_is_valid'
            ),
        }),
    )
    list_display = (
        '__str__', 'establishment', 'user', 'account_type', 'is_active', 'is_deleted', 'is_accepted', 'last_update_at'
    )
    list_filter = (
        'is_active', 'is_deleted', 'is_accepted', 'mobile_phone_is_accepted', 'mobile_phone_is_valid',
    )
    search_fields = ('last_name', 'first_name', 'account_type')

    def save_model(self, request, obj, form, change):
        obj.last_update_at = datetime.datetime.now()
        super().save_model(request, obj, form, change)


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password')
        }),
        (_('User info'), {
            'fields': ('address', 'birthday', 'country_code', 'country_name', 'gender', 'language', 'mobile_phone'),
        }),
        (_('Added fields'), {
            'fields': ('email_is_validated', 'is_deleted', 'mobile_phone_is_valid', 'mobile_phone_is_validated'),
        }),
    )
    list_display = ('__str__', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_deleted', 'last_update_at')
    list_filter = ('email_is_validated', 'gender', 'is_active', 'is_deleted', 'is_staff', 'mobile_phone_is_valid', 'mobile_phone_is_validated', 'language')
    search_fields = ('country_name', 'email', 'first_name', 'last_name', 'mobile_phone', 'username')

    def save_model(self, request, obj, form, change):
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


admin.site.register(Establishment, EstablishmentAdmin)
admin.site.register(EstablishmentUser, EstablishmentUserAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserEmailConfirmationKey, UserEmailConfirmationKeyAdmin)



