# -*- coding: utf-8 -*-

from .models import *
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class FeedsLanguageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('language', 'feeds')
        }),
    )
    list_display = ('__str__', 'language')
    list_filter = ('language',)


admin.site.register(FeedsLanguage, FeedsLanguageAdmin)



