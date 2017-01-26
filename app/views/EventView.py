from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from lib.ResourceView import ResourceView, bind_model
from app.models import Event, Registration
from app.forms import RegistrationForm, EventForm


class EventView(LoginRequiredMixin, ResourceView):
	models = [Event]

	def index(self, request):
		# Get all (unexpired) events
		events = Event.objects.prefetch_related('participants').filter(ended_at__gt=timezone.now())

		# Get a list of tuples with each event and a list of non-withdrawn participants for that event
		event_list = [(e, e.participants.filter(registration__withdrawn_at__isnull=True)) for e in events]

		return render(request, 'event_list.html', {'events': event_list})

	@bind_model
	def show(self, request, event, form=None):
		active_regs = Registration.objects.filter(event_id=event, withdrawn_at=None)
		withdrawn_regs = Registration.objects.filter(event_id=event).exclude(withdrawn_at=None)

		# Show form if deadline hasn't expired
		if not event.is_expired():
			if event.registration_set.filter(participant=request.user).exists():
				# Show update form
				registration = Registration.objects.get(event=event, participant=request.user)

				if form is None:
					form = RegistrationForm(event, data={'registered': registration.withdrawn_at is None, 'note': registration.note})

				action = reverse('registration-detail', args=[event.pk, registration.pk])
			else:
				# Show store form
				if form is None:
					form = RegistrationForm(event)

				action = reverse('registration-list', args=[event.pk])
		else:
			form = None
			action = None

		return render(request, 'event_detail.html', {
				'event': event,
				'regs': active_regs | withdrawn_regs,
				'form': form,
				'action': action
		})

	@bind_model
	def edit(self, request, event, form=None):
		self.check_user(event.committee.chairman)

		active_regs = Registration.objects.filter(event_id=event, withdrawn_at=None)
		withdrawn_regs = Registration.objects.filter(event_id=event).exclude(withdrawn_at=None)

		if form is None:
			form = EventForm(request.user, instance=event)

		return render(request, 'event_edit.html', {'event': event, 'regs': active_regs | withdrawn_regs, 'form': form})

	@bind_model
	def update(self, request, event):
		self.check_user(event.committee.chairman)

		form = EventForm(request.user, request.POST, instance=event)

		if form.is_valid():
			form.save()
			messages.success(request, "Inschrijflijst bijgewerkt!")
			return redirect('event-edit', event.pk)
		else:
			return self.edit(request, event.pk, form=form)

	def create(self, request, form=None):
		if form is None:
			form = EventForm(request.user, initial={'committee': request.GET.get('committee')})

		return render(request, 'event_create.html', {'form': form})

	def store(self, request):
		form = EventForm(request.user, request.POST)

		if form.is_valid():
			event = form.save()
			messages.success(request, "Inschrijflijst aangemaakt!")
			return redirect('event-detail', event.pk)
		else:
			return self.create(request, form=form)
