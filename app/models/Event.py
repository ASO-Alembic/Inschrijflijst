from django.db import models
from django.conf import settings
from django.utils import timezone
from .Committee import Committee
from .Registration import Registration


class Event(models.Model):
	name = models.CharField(max_length=25)
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deadline_at = models.DateTimeField(default=None, null=True, blank=True)
	ended_at = models.DateTimeField()
	event_at = models.DateTimeField()
	note_field = models.CharField(max_length=25, default='', blank=True)
	location = models.CharField(max_length=25)
	price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	committee = models.ForeignKey(Committee, on_delete=models.PROTECT)
	participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through=Registration)
	places = models.IntegerField(default=None, null=True, blank=True)

	def __str__(self):
		return self.name

	def is_expired(self):
		"""
		Return true if deadline is expired.
		"""
		return self.deadline_at is not None and self.deadline_at < timezone.now()
	class Meta:
		ordering = ['created_at']
