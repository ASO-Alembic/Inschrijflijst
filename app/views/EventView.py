from app.models import Event
from lib.ResourceView import ResourceView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class EventView(ResourceView):
	def index(self, request):
		events = Event.objects.all()

		return render(request, 'app/event_list.html', {'events': events})

