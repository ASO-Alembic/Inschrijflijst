from django import forms
from django.utils import timezone

from app.models import Registration


class RegistrationForm(forms.Form):
	registered = forms.BooleanField(
		required=False,
		label='',
		widget=forms.CheckboxInput(attrs={
			'data-toggle': 'toggle',
			'data-on': 'Ingeschreven',
			'data-off': 'Niet ingeschreven',
			'data-onstyle': 'success'
		})
	)
	note = forms.CharField(required=False, max_length=25)

	def __init__(self, event, data=None, initial=None, instance=None):
		if instance is not None:
			self.instance = instance

			# Initialise form with initial data from instance and use some other toggle labels
			super().__init__(data=data, initial={'registered': instance.withdrawn_at is None, 'note': instance.note})

			self.fields['registered'].widget = forms.CheckboxInput(attrs={
				'data-toggle': 'toggle',
				'data-on': 'Ingeschreven',
				'data-off': 'Uitgeschreven',
				'data-onstyle': 'success',
				'data-offstyle': 'danger'
			})
		else:
			super().__init__(data=data, initial=initial)

			# For a new registration, the registered field is required
			self.fields['registered'].required = True

		self.event = event

		if event.note_field != '':
			self.fields['note'].label = event.note_field
		else:
			self.fields.pop('note')

	def clean(self):
		super().clean()

		# Conditional validation rule: note field must not be empty if registered checkbox is checked and note field exists
		if self.cleaned_data['registered'] and 'note' in self.cleaned_data and self.cleaned_data['note'] == '':
			self.add_error('note', "{} niet ingevuld".format(self.event.note_field))

	def save(self, user):
		if self.instance is not None:
			registration = self.instance

			registration.note = self.cleaned_data.get('note', '')
			if self.cleaned_data['registered']:
				registration.withdrawn_at = None
			else:
				registration.withdrawn_at = timezone.now()
		else:
			registration = Registration(
				event=self.event,
				participant=user,
				note=self.cleaned_data.get('note', '')
			)

		registration.save()
