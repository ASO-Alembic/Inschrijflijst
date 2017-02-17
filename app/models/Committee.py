from django.db import models
from django.conf import settings
from django.utils.decorators import classonlymethod
from django.contrib.auth.models import User


class Committee(models.Model):
	name = models.CharField(max_length=25)
	chairman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='chaired_committees')
	email = models.EmailField()
	members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='in_committees')

	def __str__(self):
		return self.name

	@classonlymethod
	def update_committees(cls, committees):
		"""
		Update all committees in a list of dicts representing those committees.
		"""
		for c_dict in committees:
			# Create committee if it doesn't exist
			c_object, created = cls.objects.get_or_create(name=c_dict['cn'])

			# Update members
			c_object.members.set(
				[User.objects.get(username=m) for m in c_dict['members'] if User.objects.filter(username=m).exists()])

			# Update chairman and email address
			c_object.chairman = User.objects.filter(username=c_dict['chairman']).first()
			c_object.email = c_dict['email']
			c_object.save()
