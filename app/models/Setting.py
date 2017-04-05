from django.db import models


class Setting(models.Model):
	key = models.CharField(max_length=25, primary_key=True)
	value = models.TextField(blank=True)

	def save(self, *args, **kwargs):
		# Coerce None to empty string
		if self.value is None:
			self.value = ''
		super().save(*args, **kwargs)
