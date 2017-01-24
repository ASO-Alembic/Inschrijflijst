from django import forms


class MassMailForm(forms.Form):
	recipients = forms.ChoiceField(choices=[
		('active', 'Deelnemers'),
		('all', 'Deelnemers en reservelijst')
	], label='Ontvangers')
	subject = forms.CharField(max_length=25, label='Onderwerp')
	body = forms.CharField(widget=forms.Textarea(attrs={'id': 'summernote'}), initial='<p>Beste {{ name }},</p>')
