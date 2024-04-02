from django.db import models
from django.utils import timezone

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from api.models.userdata import UserData
from api.constants import constants as constants


class Audit(models.Model):
    # Audit Details
    """
    An abstract base class model that provides self updating ``created``
    and ``modified`` fields.
    """
    audit_status = models.CharField(
        choices=constants.AUDIT_STATUS, max_length=30, default='active')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        UserData, models.DO_NOTHING,
        related_name="created_%(app_label)s_%(class)s_set",
        null=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        UserData, models.DO_NOTHING,
        related_name="modified_%(app_label)s_%(class)s_set",
        null=True, editable=False)

    class Meta:
        abstract = True
