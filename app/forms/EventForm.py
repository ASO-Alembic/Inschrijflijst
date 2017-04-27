from django import forms
from bootstrap3_datetime.widgets import DateTimePicker

from app.models import Event
from app.services import GoogleCalendarService


class EventForm(forms.ModelForm):
	def __init__(self, user, data=None, initial=None, instance=None):
		super().__init__(data=data, initial=initial, instance=instance)

		self.fields['committee'].queryset = user.get_admined_committees()

		# Only show add_to_calendar field when creating new event
		if instance is not None:
			self.fields.pop('add_to_calendar')

	class Meta:
		model = Event
		fields = [
			'name',
			'description',
			'committee',
			'start_at',
			'end_at',
			'deadline_at',
			'note_field',
			'location',
			'price',
			'places',
			'add_to_calendar'
		]
		labels = {
			'name': 'Naam',
			'description': 'Beschrijving',
			'committee': 'Commissie',
			'start_at': 'Begindatumtijd',
			'end_at': 'Einddatumtijd',
			'deadline_at': 'Inschrijfdeadline',
			'note_field': 'Extra veld',
			'location': 'Locatie',
			'price': 'Kosten',
			'places': 'Beschikbare plaatsen'
		}
		widgets = {
			'deadline_at': DateTimePicker,
			'start_at': DateTimePicker,
			'end_at': DateTimePicker
		}

	add_to_calendar = forms.BooleanField(required=False, initial=True, label="Toevoegen aan jaarcirkel")

	def save(self, base_url, commit=True):
		event = super().save(commit=commit)

		if self.cleaned_data.get('add_to_calendar'):
			# Try to insert event in calendar
			try:
				cal_service = GoogleCalendarService(base_url)
				event.calendar_url = cal_service.insert_event(event)
				event.save()
			except RuntimeError:
				# Calendar not set up
				pass

		return event
