# -*- coding: utf-8 -*-
import datetime
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from colorfield.fields import ColorField
from user.models import User
from utils.utils import get_random_bg_color


class Cycle(models.Model):
    """
        Cycle represent the scholar cycles.
        :attribute: created_at: DateTimeField represent the time when the object is created.
        :attribute: created_by: ForeignKey represent the creator of the object.
        :attribute: is_active: BooleanField represent if the object is active or not
        :attribute: last_update_at: DateTimeField represent the time of last modification of object.
        :attribute: last_update_by: ForeignKey represent the last updater of the object.
        :attribute: name: CharField represent the name of the object
        :attribute: name_ar: CharField represent the arabic name of the object
        :attribute: order: IntegerField represent the order of the object
    """
    class Meta(object):
        db_table = "remedial_teaching_cycle"
        ordering = ["order"]
        verbose_name = _("Cycle")
        verbose_name_plural = _("Cycles")

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_cycles', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(_('Is active'), db_index=True, default=True)
    last_update_at = models.DateTimeField(auto_now_add=True)
    last_update_by = models.ForeignKey(User, related_name='last_modified_cycles', on_delete=models.SET_NULL, null=True)
    name = models.CharField(_('Name'), blank=False, default="", db_index=True, max_length=255, null=False, unique=True)
    name_ar = models.CharField(_('Name (ar)'), blank=True, default="", max_length=255, null=True)
    order = models.IntegerField(_('Order'), blank=False, db_index=True, null=False, unique=True)

    def __str__(self):
        return 'Cycle_' + self.name + '_' + str(self.id)

    def to_dict(self):
        """
            :return: return a representation of current instance as an object
        """
        cycle = {
            "created_at": self.created_at,
            "created_by_id": self.created_by_id,
            "id": self.id,
            "is_active": self.is_active,
            "last_update_at": self.last_update_at,
            "last_update_by_id": self.last_update_by_id,
            "name": self.name,
            "name_ar": self.name_ar,
            "order": self.order,
        }
        return cycle
