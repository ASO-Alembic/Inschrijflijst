from django.db import models
from django.conf import settings


class Registration(models.Model):
	list = models.ForeignKey('Event', on_delete=models.CASCADE)
	participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	withdrawn_at = models.DateTimeField(default=None, null=True, blank=True)
	note = models.CharField(max_length=25, default=None, null=True, blank=True)

	def __str__(self):
		return self.list.name + ' - ' + self.participant.username
