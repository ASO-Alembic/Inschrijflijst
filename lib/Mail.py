from abc import ABCMeta, abstractmethod

from django.template.loader import render_to_string
from django.template import Context, Template
from html2text import html2text
from post_office import mail


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
		self.request = None

	def get_html_body(self):
		return render_to_string(self.template, self.context, self.request)

	def get_plain_text_body(self):
		return html2text(self.get_html_body())

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

	def get_html_body(self):
		"""
		Renders the template from the given string and context and returns the message body
		"""
		html_template_string = '{{% extends "abstract/email_base.html" %}} {{% block content %}}{}{{% endblock %}}'.format(self.template_string)

		template = Template(html_template_string)
		context = Context(self.context)

		return template.render(context)


class Mailer:
	"""
	Mailer class that wraps around Django's mailing functions.
	"""
	def __init__(self, sender):
		self.sender = sender

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		pass

	def send(self, msg):
		mail.send(
			msg.get_recipients(),
			self.sender,
			subject=msg.get_subject(),
			message=msg.get_plain_text_body(),
			html_message=msg.get_html_body(),
			headers={'Reply-to': msg.get_reply_to()}
		)
