from django.db import models


class Setting(models.Model):
	key = models.CharField(max_length=25, primary_key=True)
	value = models.TextField()
