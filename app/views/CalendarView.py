from django.shortcuts import reverse, render

from app.services import GoogleCalendarService
from lib.BetterView import BetterView


class CalendarView(BetterView):
	handler_method_names = {
		'show': {'get': 'show'},
	}

	def show(self, request):
		cal_service = GoogleCalendarService(self.base_url())

		return render(request, 'calendar.html', {'calendar': cal_service.calendar})
