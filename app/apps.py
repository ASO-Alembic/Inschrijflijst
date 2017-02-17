from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save


class AppConfig(AppConfig):
	name = 'app'

	def ready(self):
		from .signals import update_committees

		post_save.connect(update_committees, settings.AUTH_USER_MODEL)
