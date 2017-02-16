from django.db import models
from django.conf import settings


class Committee(models.Model):
	name = models.CharField(max_length=25)
	chairman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='chaired_committees')
	email = models.EmailField()
	members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='in_committees')

	def __str__(self):
		return self.name
