from django.shortcuts import reverse, render

from app.services import GoogleCalendarService, FlowService
from lib.BetterView import BetterView


class CalendarView(BetterView):
	handler_method_names = {
		'show': {'get': 'show'},
	}

	def show(self, request):
		flow = FlowService(self.base_url() + reverse('admin-calendar-flow'))
		cal_service = GoogleCalendarService(flow, self.base_url())

		return render(request, 'calendar.html', {'calendar': cal_service.calendar})
