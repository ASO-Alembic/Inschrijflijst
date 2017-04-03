from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages

from lib.BetterView import BetterView, StaffRequiredMixin
from app.services import LDAPService, GoogleCalendarService, FlowService
from app.models import Committee


class AdminView(StaffRequiredMixin, BetterView):
	handler_method_names = {
		'show': {'get': 'show'},
		'sync-ldap': {'post': 'sync_ldap'},
		'calendar': {'post': 'calendar'},
		'calendar-flow': {'get': 'calendar_flow'}
	}

	def __init__(self, route, request):
		super().__init__(route, request)
		# Instantiate FlowService
		self.flow = FlowService(request.build_absolute_uri('/').strip("/") + reverse('admin-calendar-flow'))

	def show(self, request):
		# Get authorization URL for link
		authorize_url = self.flow.get_authorize_url()

		# Try to instantiate GoogleCalendarService and get list of calendars
		try:
			cal_service = GoogleCalendarService(self.flow)
			cals = cal_service.get_calendars()
			active_cal = cal_service.calendar
		except RuntimeError:
			cals = None
			active_cal = None

		return render(request, 'admin.html', {
			'authorize_url': authorize_url,
			'cals': cals,
			'active_cal': active_cal
		})

	def calendar(self, request):
		# Set 'active' calendar
		cal_service = GoogleCalendarService(self.flow)
		cal_service.calendar = request.POST['calender_id']

		messages.success(request, "Kalender ingesteld!")
		return redirect('admin')

	def calendar_flow(self, request):
		# Callback from Google

		# Finish Flow
		self.flow.exchange(request.GET['code'])

		# Empty active calendar setting
		cal_service = GoogleCalendarService(self.flow)
		cal_service.calendar = None

		messages.success(request, "Google-account gekoppeld!")
		return redirect('admin')

	def sync_ldap(self, request):
		# Get committees from AD
		with LDAPService(settings.AUTH_LDAP_SERVER_URI, settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD) as ldap_service:
			committees = ldap_service.get_committees()

		# Update all committees from list of dicts
		Committee.update_committees(committees)

		messages.success(request, "Commissies geupdatet!")
		return redirect('admin')
