from django import forms


class RegistrationForm(forms.Form):
	registered = forms.BooleanField(required=False, label='Ik ben erbij!')
	note = forms.CharField(max_length=25)

	def __init__(self, event, data=None):
		super().__init__(data=data)

		if event.note_field != '':
			self.fields['note'].label = event.note_field
		else:
			self.fields.pop('note')
