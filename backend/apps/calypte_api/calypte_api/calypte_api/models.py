from django.db import models


class UUIDAbstract(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, editable=False)

    class Meta:
        abstract = True


class TimeStampAbstract(models.Model):
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
