from abc import ABCMeta, abstractmethod

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.template import Context, Template


class Mail(metaclass=ABCMeta):
	"""
	Abstract email message class
	"""
	template = ''

	@abstractmethod
	def __init__(self):
		self.subject = ''
		self.context = {}
		self.recipients = []
		self.reply_to = ''

	def get_body(self):
		return render_to_string(self.template, self.context)

	def get_subject(self):
		return self.subject

	def get_recipients(self):
		return self.recipients

	def get_reply_to(self):
		return self.reply_to


class CustomMail(Mail):
	"""
	Mass mail with dynamic template.
	"""
	def __init__(self, reply_to, user, subject, template_string):
		"""
		Builds an email message from a user object, a sender (from address), subject and template string
		"""
		self.subject = subject
		self.context = {'name': user.first_name + ' ' + user.last_name}
		self.recipients = [user.email]
		self.reply_to = [reply_to]
		self.template_string = template_string

	def get_body(self):
		"""
		Renders the template from the given string and context and returns the message body
		"""
		template = Template(self.template_string)
		context = Context(self.context)

		return template.render(context)


class Mailer:
	"""
	Mailer class that wraps around Django's mailing functions. Is a context manager for a connection.
	"""
	def __init__(self, sender):
		self.sender = sender
		self.connection = get_connection()
		self.connection.open()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.connection.close()

	def send(self, mail):
		msg = EmailMessage(
			mail.get_subject(),
			mail.get_body(),
			self.sender,
			mail.get_recipients(),
			reply_to=mail.get_reply_to(),
			connection=self.connection
		)

		msg.content_subtype = 'html'
		msg.send()
