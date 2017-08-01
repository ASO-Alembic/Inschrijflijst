from django.db import models
from django.forms import CharField


class CommaSeparatedCharField(CharField):

	def prepare_value(self, value):
		"""Convert list to comma-separated string"""
		if value in self.empty_values:
			return ''

		return ','.join(value)

	def to_python(self, value):
		"""Convert comma-separated string to list"""
		if value in self.empty_values:
			return []

		return value.split(',')

	def widget_attrs(self, widget):
		attrs = super().widget_attrs(widget)
		attrs['data-role'] = 'tagsinput'
		return attrs


class CommaSeparatedStringsField(models.CharField):
	description = "Stores list as string of comma-separated strings"

	def from_db_value(self, value, *args):
		if not value:
			return []

		return value.split(',')

	def to_python(self, value):
		if isinstance(value, list):
			return value

		return self.from_db_value(value)

	def get_prep_value(self, value):
		return ','.join(value)

	def value_to_string(self, obj):
		return self.get_prep_value(self.value_from_object(obj))

	def formfield(self, **kwargs):
		defaults = {'form_class': CommaSeparatedCharField}
		defaults.update(kwargs)

		return models.Field.formfield(self, **defaults)
