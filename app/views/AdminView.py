from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from lib.BetterView import BetterView, StaffRequiredMixin
from app.services.LDAPService import LDAPService
from app.models.Committee import Committee


class AdminView(StaffRequiredMixin, BetterView):
	handler_method_names = {
		'show': {'get': 'show'},
		'sync-ldap': {'post': 'sync_ldap'}
	}

	def show(self, request):
		return render(request, 'admin.html')

	def sync_ldap(self, request):
		# Get committees from AD
		with LDAPService(settings.AUTH_LDAP_SERVER_URI, settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD) as ldap_service:
			committees = ldap_service.get_committees()

		# Update all committees from list of dicts
		Committee.update_committees(committees)

		messages.success(request, "Commissies geupdatet!")
		return redirect('admin')
