from django.conf import settings

from app.services.LDAPService import LDAPService
from app.models.Committee import Committee


def update_committees(sender, **kwargs):
	"""
	Update all committees the user is involved in when the user first logs in.
	"""
	if kwargs['created']:
		with LDAPService(settings.AUTH_LDAP_SERVER_URI, settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD) as ldap_service:
			committees = ldap_service.get_in_committees(kwargs['instance'].username)

		# Update all committees from list of dicts
		Committee.update_committees(committees)
