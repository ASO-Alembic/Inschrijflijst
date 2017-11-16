from django.shortcuts import render

from app.services import GoogleCalendarService
from lib.BetterView import BetterView


class CalendarView(BetterView):
	handler_method_names = {
		'show': {'get': 'show'},
	}

	def show(self, request):
		cal_service = GoogleCalendarService(request.base_url)

		return render(request, 'calendar.html', {'calendar': cal_service.calendar})
