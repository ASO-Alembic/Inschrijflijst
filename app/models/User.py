from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
	class Meta(AbstractUser.Meta):
		swappable = 'AUTH_USER_MODEL'
		db_table = 'auth_user'

	last_seen_at = models.DateTimeField(default=None, null=True)
	email = models.EmailField(_('email address'))

	def is_admin(self):
		"""
		Return true if user is committee admin (either by being chairman or by being member of a committee that has super members)
		"""
		return self.chaired_committees.exists() or self.in_committees.filter(super_members=True).exists()

	def is_admin_of_committee(self, committee):
		"""
		Return true if the user is admin of given committee.
		"""
		return committee in self.get_admined_committees()

	def get_admined_committees(self):
		"""
		Return all committees the users is admin of (the union of chaired committees and the committees the user is super member of)
		"""
		return (self.chaired_committees.all() | self.in_committees.filter(super_members=True)).distinct()
