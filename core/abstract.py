
from django.db import models


class AbstractTimestamp(models.Model):
    """
    Time track model entries.

    Use mostly on transactional data to track latest changes.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AbstractAuthority(models.Model):
    """
    Track Data Authority of respective model data

    Use this class for logging and tracking models under person and department
    """

    created_by = models.ForeignKey(
        "core.BaseUser",
        on_delete=models.PROTECT,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
        blank=True,
    )
    updated_by = models.ForeignKey(
        "core.BaseUser",
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_updated",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True