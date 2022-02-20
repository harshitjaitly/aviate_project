from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone



class CustomQuerySet(QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    ``date_deleted``, effectively soft-deleting the object.
    """

    def delete(self):
        for obj in self:
            obj.deleted_on=timezone.now()
            obj.save()


class CustomManager(models.Manager):
    """
    A Manager which exposes Profile objects that have NOT been soft-deleted.
    """

    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db).filter(
            deleted_on__isnull=True)

class CustomModel(models.Model):
    class Meta:
        abstract = True

    deleted_on = models.DateTimeField(editable=False,null=True, blank=True)
    objects = CustomManager()
    original_objects = models.Manager()

    def delete(self):
        self.deleted_on=timezone.now()
        self.save()
