from django import forms
from django.utils import timezone
from bootstrap3_datetime.widgets import DateTimePicker
from django_auth_ldap.backend import LDAPBackend

from app.models import User, Registration
from app.mails import RegistrationNotificationMail


class RegistrationsForm(forms.Form):
	username = forms.CharField(label='Gebruikersnaam', widget=forms.TextInput(attrs={'list': 'usernames'}))
	date = forms.DateField(initial=timezone.now(), widget=DateTimePicker)

	def __init__(self, event, **kwargs):
		super().__init__(**kwargs)

		self.event = event

		# Add CharField or ChoiceField depending if note options are set in event
		if event.note_field != '':
			if not event.note_field_options:
				self.fields['note'] = forms.CharField(max_length=25, label=event.note_field, required=event.note_field_required)
			else:
				self.fields['note'] = forms.ChoiceField(choices=event.get_note_field_options(), label=event.note_field, required=event.note_field_required)

	def clean_username(self):
		"""
		Verify that the username is correct (exists in LDAP) and return user object
		"""
		# Try to retrieve user from dbase, or create one and populate from LDAP if it does not exist
		try:
			user = User.objects.get(username=self.cleaned_data['username'])
		except User.DoesNotExist:
			user = LDAPBackend().populate_user(self.cleaned_data['username'])

			# Raise ValidationError if username does not exist in LDAP
			if user is None:
				raise forms.ValidationError("Gebruikersnaam {} is niet bekend".format(self.cleaned_data['username']))

		return user

	def save(self, mailer, request):
		registration, created = Registration.objects.get_or_create(
			event=self.event,
			participant=self.cleaned_data['username']
		)

		registration.note = self.cleaned_data.get('note', '')
		registration.created_at = self.cleaned_data.get('date', timezone.now())
		registration.withdrawn_at = None
		registration.save()

		# Send mail to participant
		mailer.send(RegistrationNotificationMail(self.event, self.cleaned_data['username'], request))
