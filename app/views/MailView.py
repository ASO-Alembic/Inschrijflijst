from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.translation import ugettext as _

from lib.ResourceView import ResourceView, bind_model
from lib.Mail import CustomMail, Mailer
from app.models import Event
from app.forms import MassMailForm


class MailView(LoginRequiredMixin, ResourceView):
	models = [Event]

	@bind_model
	def create(self, request, event, form=None):
		self.check_admin_of(event.committee)

		if form is None:
			form = MassMailForm

		return render(request, 'mail_create.html', {'event': event, 'form': form})

	@bind_model
	def store(self, request, event):
		self.check_admin_of(event.committee)

		form = MassMailForm(data=request.POST)

		# Counter
		i = 0

		if form.is_valid():
			with Mailer(settings.DEFAULT_FROM_EMAIL) as mailer:
				for reg in event.registration_set.filter(withdrawn_at=None):
					# Only send mail if not withdrawn, and send mail to backup depending on form setting
					if not reg.is_backup() or form.cleaned_data['recipients'] == 'all':
						msg = CustomMail(event.committee.email, reg.participant, form.cleaned_data['subject'], form.cleaned_data['body'])
						mailer.send(msg)
						i += 1
		else:
			return self.create(request, event.pk, form=form)

		messages.success(request, _("{} emails verstuurd!").format(i))
		return redirect('mail-create', event.pk)
