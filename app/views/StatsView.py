import datetime

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from lib.BetterView import BetterView
from app.models import Event


class StatsView(LoginRequiredMixin, BetterView):
	handler_method_names = {
		'registrations': {'get': 'get_registrations'}
	}

	def get_registrations(self, request, event_id):
		event = get_object_or_404(Event, pk=event_id)

		with connection.cursor() as cursor:
			cursor.execute("SELECT DATE_FORMAT(created_at, '%%Y-%%m-%%d') AS date, COUNT(*) AS count FROM app_registration WHERE withdrawn_at IS NULL AND event_id = %s GROUP BY date", [event_id])
			# Fetch and convert tuple of (date, count) to dict of {date: count}
			result = {date: count for date, count in cursor.fetchall()}

		# Generate list of dates in range of event
		date_list = ((event.created_at + datetime.timedelta(days=x)).date() for x in range(0, (event.deadline_at - event.created_at).days))

		# Return list of dicts in correct format for Chart.js
		chartdata = [{'x': date, 'y': result.get(str(date), 0)} for date in date_list]

		return JsonResponse(chartdata, safe=False)
