from django.forms import ModelForm
from bootstrap3_datetime.widgets import DateTimePicker

from app.models import Event


class EventForm(ModelForm):
	def __init__(self, user, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['committee'].queryset = user.committee_set

	class Meta:
		model = Event
		fields = [
			'name',
			'description',
			'committee',
			'event_at',
			'deadline_at',
			'ended_at',
			'note_field',
			'location',
			'price',
			'places'
		]
		labels = {
			'name': 'Naam',
			'description': 'Beschrijving',
			'committee': 'Commissie',
			'event_at': 'Datum',
			'deadline_at': 'Inschrijfdeadline',
			'ended_at': 'Einddatum',
			'note_field': 'Extra veld',
			'location': 'Locatie',
			'price': 'Kosten',
			'places': 'Beschikbare plaatsen'
		}
		widgets = {
			'deadline_at': DateTimePicker,
			'ended_at': DateTimePicker,
			'event_at': DateTimePicker
		}
