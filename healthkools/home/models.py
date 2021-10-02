# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
import json


class FeedsLanguage(models.Model):
    """
        UserAccountType represent the FeedsLanguage model.
    """
    class Meta(object):
        db_table = "healthkools_feeds_language"
        verbose_name = _("Feeds language")
        verbose_name_plural = _("Feeds languages")

    feeds = models.TextField(_('Feeds'), default="")
    language = models.CharField(_('Language'), choices=settings.LANGUAGES, default="fr", max_length=255, unique=True)

    def __str__(self):
        return self.language + "_feeds"

    def to_items_list(self):
        return json.loads(self.feeds or '[]')
