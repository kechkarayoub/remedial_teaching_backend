# -*- coding: utf-8 -*-

from .models import *
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class FeedsLanguageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('language', 'feeds')
        }),
    )
    list_display = ('language', 'last_update')
    list_filter = ('language',)


admin.site.register(FeedsLanguage, FeedsLanguageAdmin)



