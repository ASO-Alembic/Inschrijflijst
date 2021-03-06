from lib.Mail import Mail
from django.utils.translation import ugettext as _


class RegistrationNotificationMail(Mail):
	template = 'mails/registration_notification.html'

	def __init__(self, event, recipient_user, request):
		self.request = request
		self.subject = _("Ingeschreven voor {}").format(event.name)
		self.context = {
			'recipient': recipient_user.first_name + ' ' + recipient_user.last_name,
			'sender': request.user.first_name + ' ' + request.user.last_name,
			'event': event
		}
		self.recipients = [recipient_user.email]
		self.reply_to = request.user.email

		self.validate()
