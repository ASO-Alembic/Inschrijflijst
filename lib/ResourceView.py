from abc import ABCMeta


from django.conf.urls import url
from django.shortcuts import get_object_or_404

from .BetterView import BetterView


class ResourceView(BetterView, metaclass=ABCMeta):
	"""
	Simple Laravel-style RESTful resource controller/view base class.
	Is actually a thin wrapper around BetterView specifically for views that directly correspond to a model.
	Intended to be used with ResourceRouter for automatically generating URLconf for a ResourceView.
	"""
	# List of model names for model binding (see decorator below), in hiearchical order
	models = []

	# 2d lookup table with routes and HTTP methods, returns name of handler method
	# a 'route' in this case is an unique URL pattern
	handler_method_names = {
		'index': {
			'get': 'index',
			'post': 'store'
		},
		'show': {
			'get': 'show',
			'put': 'update',
			'delete': 'destroy'
		},
		'create': {
			'get': 'create'
		},
		'edit': {
			'get': 'edit'
		}
	}

	# Handler methods, should be overridden in child class

	def index(self, request, *args):
		raise NotImplementedError

	def store(self, request, *args):
		raise NotImplementedError

	def show(self, request, *args):
		raise NotImplementedError

	def update(self, request, *args):
		raise NotImplementedError

	def destroy(self, request, *args):
		raise NotImplementedError

	def create(self, request, *args):
		raise NotImplementedError

	def edit(self, request, *args):
		raise NotImplementedError


def bind_model(func):
	"""
	Decorator for automatically retrieving model instances from database; instead of ids, the models instances are injected.
	Requires the model property to be set in the view class.
	Attempts to retrieve model instances for all *args, leaves **kwargs untouched.
	"""
	def decorator(self, request, *args, **kwargs):
		# Instantiate a model for every passed argument, using self.models to look up the model class
		objects = [get_object_or_404(self.models[i], pk=v) for i, v in enumerate(args)]

		return func(self, request, *objects, **kwargs)

	return decorator


class ResourceRouter:
	"""
	Basic router for automatically generating URLconf patterns for use with ResourceView.
	"""
	def __init__(self):
		self.resources = []

	def register(self, nodes, view, name):
		"""
		Register a new ResourceView.
		Nodes should be an list of (plural) resource nodes.
		"""
		self.resources.append((nodes, view, name))

	def urls(self):
		"""
		Generate a list of URL patterns from the registered routes.
		"""
		ret = []

		for nodes, view, name in self.resources:
			# Pop of the endpoint in the list of resource nodes
			endpoint = nodes.pop()

			# Build prefix string
			prefix_string = '^'
			for node in nodes:
				prefix_string += r'{}/(\d+)/'.format(node)

			list_url = url(
				prefix_string + r'{}/$'.format(endpoint),
				view.as_view('index'),
				name='{}-list'.format(name)
			)

			create_url = url(
				prefix_string + r'{}/create$'.format(endpoint),
				view.as_view('create'),
				name='{}-create'.format(name)
			)

			detail_url = url(
				prefix_string + r'{}/(\d+)$'.format(endpoint),
				view.as_view('show'),
				name='{}-detail'.format(name)
			)

			edit_url = url(
				prefix_string + r'{}/(\d+)/edit$'.format(endpoint),
				view.as_view('edit'),
				name='{}-edit'.format(name)
			)

			ret.extend([list_url, create_url, detail_url, edit_url])

		return ret
