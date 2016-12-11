from django.forms import ModelForm
from app.models import Event


class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = [
			'name',
			'description',
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
			'deadline_at': 'Inschrijfdeadline',
			'ended_at': 'Einddatum',
			'note_field': 'Extra veld',
			'location': 'Locatie',
			'price': 'Kosten',
			'places': 'Beschikbare plaatsen'
		}
