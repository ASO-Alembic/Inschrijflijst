from django import forms
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from bootstrap3_datetime.widgets import DateTimePicker

from app.models import Event
from app.services import GoogleCalendarService, FCMService
from lib.Mail import Mailer


class EventForm(forms.ModelForm):
	def __init__(self, user, data=None, initial=None, instance=None):
		super().__init__(data=data, initial=initial, instance=instance)

		self.fields['committee'].queryset = user.get_admined_committees()

		# Only show add_to_calendar, enroll_committee and send_notification fields when creating new event
		if instance is not None:
			self.fields.pop('add_to_calendar')
			self.fields.pop('enroll_committee')
			self.fields.pop('send_notification')

	class Meta:
		model = Event
		fields = [
			'name',
			'description',
			'long_description',
			'committee',
			'start_at',
			'end_at',
			'deadline_at',
			'published_at',
			'note_field',
			'note_field_options',
			'note_field_required',
			'note_field_public',
			'location',
			'price',
			'places',
			'add_to_calendar'
		]
		labels = {
			'name':                 _('Naam'),
			'description':          _("Beschrijving"),
			'long_description':     _("Lange beschrijving"),
			'committee':            _("Commissie"),
			'start_at':             _("Begindatumtijd"),
			'end_at':               _("Einddatumtijd"),
			'deadline_at':          _("Inschrijfdeadline"),
			'published_at':         _("Publicatiedatum"),
			'note_field':           _("Titel"),
			'note_field_options':   _("Opties"),
			'note_field_required':  _("Verplicht"),
			'note_field_public':    _("Antwoord publiek zichtbaar"),
			'location':             _("Locatie"),
			'price':                _("Kosten"),
			'places':               _("Beschikbare plaatsen")
		}
		widgets = {
			'deadline_at':  DateTimePicker,
			'start_at':     DateTimePicker,
			'end_at':       DateTimePicker,
			'published_at': DateTimePicker
		}

	add_to_calendar = forms.BooleanField(required=False, initial=True, label=_("Toevoegen aan jaarcirkel"))
	enroll_committee = forms.BooleanField(required=False, initial=False, label=_("Schrijf je commissie in"))
	send_notification = forms.BooleanField(required=False, initial=True, label=_("Stuur notificatie naar app gebruikers"))

	def save(self, request, commit=True):
		# The request object is needed for two things here: the base_url and the email message
		# I don't really like the approach of passing around the request but I don't know anything better either

		event = super().save(commit=commit)

		if self.cleaned_data.get('add_to_calendar'):
			# Try to insert event in calendar
			try:
				cal_service = GoogleCalendarService(request.base_url)
				event.calendar_url = cal_service.insert_event(event)
				event.save()
			except RuntimeError:
				# Calendar not set up
				pass

		# Send notification to app users
		if self.cleaned_data.get('send_notification'):
			try:
				fcm_service = FCMService(request.base_url)
				fcm_service.notify(event)
			except RuntimeError:
				messages.error(request, _("Notification message not sent."))

		if self.cleaned_data.get('enroll_committee'):
			# Enroll committee
			self.cleaned_data.get('committee').enroll(Mailer(settings.DEFAULT_FROM_EMAIL), event, request)

		return event
