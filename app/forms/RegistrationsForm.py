from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from bootstrap3_datetime.widgets import DateTimePicker
from django_auth_ldap.backend import LDAPBackend


class RegistrationsForm(forms.Form):
	username = forms.CharField(label='Gebruikersnaam', widget=forms.TextInput(attrs={'list': 'usernames'}))
	note = forms.CharField(max_length=25)
	date = forms.DateField(initial=timezone.now(), widget=DateTimePicker)

	def __init__(self, event, **kwargs):
		super().__init__(**kwargs)

		if event.note_field != '':
			self.fields['note'].label = event.note_field
		else:
			self.fields.pop('note')

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
