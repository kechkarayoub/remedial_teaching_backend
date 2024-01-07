# -*- coding: utf-8 -*-

from .models import *
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


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
    list_display = ('__str__', 'name', 'is_active', 'is_deleted', 'last_update_at', 'last_update_by')
    list_filter = (
        'is_active', 'is_deleted', 'type', 'city', 'mobile_phone_is_valid', 'mobile_phone_is_validated',
        'phone_is_valid', 'phone_is_validated', 'phone2_is_valid', 'phone2_is_validated',
    )
    search_fields = ('name', 'name_ar', 'address', 'address_ar', 'city')

    def save_model(self, request, obj, form, change):
        if request.user:
            if not obj.id:
                obj.created_by = request.user
            obj.last_update_by = request.user
        obj.last_update_at = datetime.datetime.now()
        super().save_model(request, obj, form, change)


class EstablishmentGroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name', 'name_ar', 'is_active', 'is_deleted', 'logo_url',
            )
        }),
    )
    list_display = ('__str__', 'name', 'is_active', 'is_deleted', 'last_update_at', 'last_update_by')
    list_filter = (
        'is_active', 'is_deleted',
    )
    search_fields = ('name', 'name_ar', )

    def save_model(self, request, obj, form, change):
        if request.user:
            if not obj.id:
                obj.created_by = request.user
            obj.last_update_by = request.user
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
                'mobile_phone', 'image_url', 'initials_bg_color',
            )
        }),
        (_('Added fields'), {
            'fields': (
                'email_is_accepted', 'mobile_phone_is_accepted', 'mobile_phone_is_valid'
            ),
        }),
    )
    list_display = (
        '__str__', 'establishment', 'user', 'account_type', 'is_active', 'is_deleted', 'is_accepted', 'last_update_at',
        'last_update_by'
    )
    list_filter = (
        'is_active', 'is_deleted', 'is_accepted', 'mobile_phone_is_accepted', 'mobile_phone_is_valid',
    )
    search_fields = ('last_name', 'first_name', 'account_type')

    def save_model(self, request, obj, form, change):
        if request.user:
            if not obj.id:
                obj.created_by = request.user
            obj.last_update_by = request.user
        obj.last_update_at = datetime.datetime.now()
        super().save_model(request, obj, form, change)


class ScholarYearAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name', 'short_name', 'order', 'start_year', 'is_active', 'is_current', 'is_deleted',
                'date_start', 'date_end',
            )
        }),
    )
    list_display = (
        '__str__', 'short_name', 'order', 'start_year', 'is_active', 'is_current', 'is_deleted',
        'last_update_at', 'last_update_by',
    )
    list_filter = (
        'is_active', 'is_deleted', 'is_current',
    )
    search_fields = ('name', 'short_name',)

    def save_model(self, request, obj, form, change):
        if request.user:
            if not obj.id:
                obj.created_by = request.user
            obj.last_update_by = request.user
        obj.last_update_at = datetime.datetime.now()
        super().save_model(request, obj, form, change)


admin.site.register(Establishment, EstablishmentAdmin)
admin.site.register(EstablishmentGroup, EstablishmentGroupAdmin)
admin.site.register(EstablishmentUser, EstablishmentUserAdmin)
admin.site.register(ScholarYear, ScholarYearAdmin)



