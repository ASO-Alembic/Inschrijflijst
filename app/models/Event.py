from django.db import models
from django.conf import settings
from .Committee import Committee
from .Registration import Registration


class Event(models.Model):
	name = models.CharField(max_length=25)
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deadline_at = models.DateTimeField(default=None, null=True, blank=True)
	ended_at = models.DateTimeField()
	committee = models.ForeignKey(Committee, on_delete=models.PROTECT)
	participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through=Registration)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['created_at']
