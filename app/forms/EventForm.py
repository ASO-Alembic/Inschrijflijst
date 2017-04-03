from django.forms import ModelForm
from bootstrap3_datetime.widgets import DateTimePicker

from app.models import Event


class EventForm(ModelForm):
	def __init__(self, user, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['committee'].queryset = user.get_admined_committees()

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
			'places'
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
