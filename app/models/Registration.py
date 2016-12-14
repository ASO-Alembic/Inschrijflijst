from django.db import models, transaction, IntegrityError
from django.conf import settings


class Registration(models.Model):
	event = models.ForeignKey('Event', on_delete=models.CASCADE)
	participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	withdrawn_at = models.DateTimeField(default=None, null=True, blank=True)
	note = models.CharField(max_length=25, default=None, null=True, blank=True)

	def __str__(self):
		return self.event.name + ' - ' + self.participant.username

	@transaction.atomic
	def save(self, *args, **kwargs):
		"""
		Ensure that the number of non-withdrawn registrations can never exceed the number of places of the event.
		"""
		super().save(*args, **kwargs)

		if self.event.places is not None and self.event.get_free_places() < 0:
			# Rollback transaction
			raise IntegrityError('Inschrijflijst vol')

	class Meta:
		ordering = ['created_at']
		unique_together = ('event', 'participant')
