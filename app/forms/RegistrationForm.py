from django import forms


class RegistrationForm(forms.Form):
	registered = forms.BooleanField(required=False, label='Ik ben erbij!')
	note = forms.CharField(required=False, max_length=25)

	def __init__(self, event, data=None):
		super().__init__(data=data)

		self.event = event

		if event.note_field != '':
			self.fields['note'].label = event.note_field
		else:
			self.fields.pop('note')

	def clean(self):
		super().clean()

		# Conditional validation rule: note field must not be empty if registered checkbox is checked and note field exists
		if self.cleaned_data['registered'] and 'note' in self.cleaned_data and self.cleaned_data['note'] == '':
			self.add_error('note', "{} niet ingevuld".format(self.event.note_field))
