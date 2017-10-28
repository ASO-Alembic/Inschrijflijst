from django.db import models
from django.conf import settings


class Registration(models.Model):
	event = models.ForeignKey('Event', on_delete=models.CASCADE)
	participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	withdrawn_at = models.DateTimeField(default=None, null=True, blank=True)
	note = models.CharField(max_length=100, default='', blank=True)

	def __str__(self):
		return self.event.name + ' - ' + self.participant.username

	def is_backup(self):
		"""
		Return true if this is a 'backup registration' (registered after the event was full)
		"""
		# Find position of registration in event by counting all preceding active registrations
		position = self.event.registration_set.filter(updated_at__lte=self.updated_at, withdrawn_at__isnull=True).count()

		return self.event.places is not None and position > self.event.places

	class Meta:
		ordering = ['updated_at']
		unique_together = ('event', 'participant')
