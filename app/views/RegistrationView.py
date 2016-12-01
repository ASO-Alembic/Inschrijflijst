from lib.ResourceView import ResourceView, bind_model
from app.models import Event, Registration
from app.forms import RegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.utils import timezone


class RegistrationView(LoginRequiredMixin, ResourceView):
	models = [Event, Registration]

	@bind_model
	def store(self, request, event):
		form = RegistrationForm(event, request.POST)

		# For a new registration, the registered field is required
		form.fields['registered'].required = True

		if form.is_valid():
			registration = Registration(
				event=event,
				participant=request.user,
				note=form.cleaned_data.get('note', '')
			)

			registration.save()

			return redirect('event-detail', event.pk)

		# TODO: Handle validation errors

	@bind_model
	def update(self, request, event, registration):
		form = RegistrationForm(event, request.POST)

		if form.is_valid():
			# Make sure the user is updating their own registration
			if registration.participant != request.user:
				raise PermissionDenied

			registration.note = form.cleaned_data.get('note', '')

			if form.cleaned_data['registered']:
				registration.withdrawn_at = None
			else:
				registration.withdrawn_at = timezone.now()

			registration.save()

			return redirect('event-detail', event.pk)
