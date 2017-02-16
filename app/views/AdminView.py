from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User

from app.services.LDAPService import LDAPService
from app.models.Committee import Committee


def get(request):
	return render(request, 'admin.html')


def sync_ldap(request):
	with LDAPService(settings.AUTH_LDAP_SERVER_URI, settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD) as ldap_service:
		committees = ldap_service.get_committees()

	for c_dict in committees:
		# Create committee if it doesn't exist
		c_object, created = Committee.objects.get_or_create(name=c_dict['cn'])

		# Update members
		c_object.members.set([User.objects.get(username=m) for m in c_dict['members'] if User.objects.filter(username=m).exists()])

		# Update chairman
		c_object.chairman = User.objects.filter(username=c_dict['chairman']).first()
		c_object.save()

	messages.success(request, "Commissies geupdatet!")
	return redirect('admin')
