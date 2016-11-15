from django.db import models
from django.conf import settings


class Committee(models.Model):
	name = models.CharField(max_length=25)
	chairman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
