from lib.ResourceView import ResourceView, bind_model
from app.models import Event, Registration
from app.forms import RegistrationForm
from django.shortcuts import render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class EventView(LoginRequiredMixin, ResourceView):
	models = [Event]

	def index(self, request):
		events = Event.objects.all()

		return render(request, 'app/event_list.html', {'events': events})

	@bind_model
	def show(self, request, event):
		active_regs = Registration.objects.filter(event_id=event, withdrawn_at=None)
		withdrawn_regs = Registration.objects.filter(event_id=event).exclude(withdrawn_at=None)

		if request.user in event.participants.all():
			# Show update form
			registration = Registration.objects.get(event=event, participant=request.user)
			form = RegistrationForm(event, data={'registered': registration.withdrawn_at is None, 'note': registration.note})
			action = reverse('registration-detail', args=[event.pk, registration.pk])
		else:
			# Show store form
			form = RegistrationForm(event)
			action = reverse('registration-list', args=[event.pk])

		return render(request, 'app/event_detail.html', {
				'event': event,
				'regs': active_regs | withdrawn_regs,
				'form': form,
				'action': action
		})
