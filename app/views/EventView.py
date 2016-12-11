from lib.ResourceView import ResourceView, bind_model
from app.models import Event, Registration
from app.forms import RegistrationForm, EventForm
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core.exceptions import PermissionDenied


class EventView(LoginRequiredMixin, ResourceView):
	models = [Event]

	def index(self, request):
		# Get a list of tuples with each event and a bool denoting whether the user is registered (and not withdrawn) for it
		events = [(e, e.registration_set.filter(participant=request.user, withdrawn_at__isnull=True).exists())
		          for e in Event.objects.prefetch_related('registration_set').all()]

		return render(request, 'app/event_list.html', {'events': events})

	@bind_model
	def show(self, request, event):
		active_regs = Registration.objects.filter(event_id=event, withdrawn_at=None)
		withdrawn_regs = Registration.objects.filter(event_id=event).exclude(withdrawn_at=None)

		# Show form if deadline hasn't expired
		if not event.is_expired():
			if request.user in event.participants.all():
				# Show update form
				registration = Registration.objects.get(event=event, participant=request.user)
				form = RegistrationForm(event, data={'registered': registration.withdrawn_at is None, 'note': registration.note})
				action = reverse('registration-detail', args=[event.pk, registration.pk])
			else:
				# Show store form
				form = RegistrationForm(event)
				action = reverse('registration-list', args=[event.pk])
		else:
			form = None
			action = None

		return render(request, 'app/event_detail.html', {
				'event': event,
				'regs': active_regs | withdrawn_regs,
				'form': form,
				'action': action
		})

	@bind_model
	def edit(self, request, event):
		if event.committee.chairman != request.user:
			raise PermissionDenied

		active_regs = Registration.objects.filter(event_id=event, withdrawn_at=None)
		withdrawn_regs = Registration.objects.filter(event_id=event).exclude(withdrawn_at=None)
		form = EventForm(instance=event)

		return render(request, 'app/event_edit.html', {'event': event, 'regs': active_regs | withdrawn_regs, 'form': form})

	@bind_model
	def update(self, request, event):
		if event.committee.chairman != request.user:
			raise PermissionDenied

		form = EventForm(request.POST, instance=event)

		if form.is_valid():
			form.save()
			return redirect('event-edit', event.pk)

