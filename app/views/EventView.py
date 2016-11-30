from lib.ResourceView import ResourceView, bind_model
from app.models import Event, Registration
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


class EventView(LoginRequiredMixin, ResourceView):
	models = [Event]

	def index(self, request):
		events = Event.objects.all()

		return render(request, 'app/event_list.html', {'events': events})

	@bind_model
	def show(self, request, event):
		active_regs = Registration.objects.filter(event_id=event.pk, withdrawn_at=None)
		withdrawn_regs = Registration.objects.filter(event_id=event.pk).exclude(withdrawn_at=None)

		return render(request, 'app/event_detail.html', {'event': event, 'regs': active_regs | withdrawn_regs})
