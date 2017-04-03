from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.urls import reverse

from .Committee import Committee
from .Registration import Registration


class Event(models.Model):
	name = models.CharField(max_length=25)
	description = models.TextField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deadline_at = models.DateTimeField(default=None, null=True, blank=True)
	start_at = models.DateTimeField()
	end_at = models.DateTimeField()
	note_field = models.CharField(max_length=25, default='', blank=True)
	location = models.CharField(max_length=25)
	price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	calendar_url = models.CharField(max_length=255, blank=True)
	committee = models.ForeignKey(Committee, on_delete=models.PROTECT)
	participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through=Registration)
	places = models.PositiveIntegerField(default=None, null=True, blank=True, validators=[MinValueValidator(1)])

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('event-detail', args=[self.pk])

	def is_expired(self):
		"""
		Return true if deadline is expired.
		"""
		return self.deadline_at is not None and self.deadline_at < timezone.now()

	def is_full(self):
		"""
		Return true if there are no free places left.
		"""
		return self.get_free_places() is not None and self.get_free_places() <= 0

	def get_free_places(self):
		"""
		Return the number of free places left.
		"""
		if self.places is None:
			# If the event doesn't have a places limit, the value of this function is not defined
			return None
		else:
			return self.places - Registration.objects.filter(event=self, withdrawn_at__isnull=True).count()

	def get_active_registrations_count(self):
		"""
		Return the number of non-withdrawn registrations
		"""
		return self.registration_set.filter(withdrawn_at__isnull=True).count()

	class Meta:
		ordering = ['created_at']
