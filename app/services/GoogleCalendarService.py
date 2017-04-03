import httplib2

from oauth2client import client
from oauth2client.file import Storage
from googleapiclient.discovery import build

from app.models import Setting


class GoogleCalendarService:
	"""
	Service for communicating with Google Calendar API.
	"""
	def __init__(self, flow, base_url):
		"""
		Get credentials from injected FlowService and setup service
		"""
		self.base_url = base_url
		self.credentials = flow.get_credentials()

		http = self.credentials.authorize(httplib2.Http())
		self.service = build('calendar', 'v3', http=http)

	def get_calendars(self):
		"""
		Retrieves list of all (writeable) calendars and returns it as dict.
		"""
		result = self.service.calendarList().list(minAccessRole='writer').execute()

		return {cal['id']: cal['summary'] for cal in result['items']}

	@property
	def calendar(self):
		"""
		Return 'active' calendar or None if it is not set
		"""
		try:
			return Setting.objects.get(key='calendar_id').value
		except Setting.DoesNotExist:
			return None

	@calendar.setter
	def calendar(self, calendar_id):
		"""
		Set 'active' calendar by saving it in Setting table
		"""
		Setting.objects.update_or_create(key='calendar_id', defaults={'value': calendar_id})

	def insert_event(self, app_event):
		"""
		Create and insert calendar event from App event
		"""
		cal_event = {
			'summary': app_event.name,
			'location': app_event.location,
			'description': self.base_url + app_event.get_absolute_url(),
			'start': {
				'dateTime': app_event.start_at.isoformat(),
			},
			'end': {
				'dateTime': app_event.end_at.isoformat(),
			},
		}

		# Insert calendar event
		result = self.service.events().insert(calendarId=self.calendar, body=cal_event).execute()

		# Update app event with calendar URL
		app_event.calendar_url = result['htmlLink']
		app_event.save()


class FlowService:
	"""
	Service for Google OAuth2 API
	"""
	SCOPES = 'https://www.googleapis.com/auth/calendar'
	CLIENT_SECRET_FILE = 'storage/client_id.json'
	CREDENTIALS_FILE = 'storage/credentials.json'

	def __init__(self, redirect_uri):
		"""
		Instantiate Flow object from client secrets
		"""
		self.flow = client.flow_from_clientsecrets(
			filename=self.CLIENT_SECRET_FILE,
			scope=self.SCOPES,
			redirect_uri=redirect_uri
		)
		self.flow.params['access_type'] = 'offline'

	def get_authorize_url(self):
		return self.flow.step1_get_authorize_url()

	def exchange(self, code):
		credentials = self.flow.step2_exchange(code)
		store = Storage(self.CREDENTIALS_FILE)
		store.put(credentials)

	def get_credentials(self):
		store = Storage(self.CREDENTIALS_FILE)
		credentials = store.get()

		if not credentials or credentials.invalid:
			raise RuntimeError('Credentials invalid')

		return credentials
