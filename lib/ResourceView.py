from django import http
from django.conf.urls import url
from django.utils.decorators import classonlymethod
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


class ResourceView:
	"""
	Simple Laravel-style RESTful resource controller/view base class.
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
		'create': {'get': 'create'},
		'edit': {'get': 'edit'}
	}

	def __init__(self, route, request):
		"""
		Constructor (called for every single request in the function generated by as_view)
		Store route variable in instance so that dispatch() can access it.
		"""
		self.route = route
		self.request = request

	@classonlymethod
	def as_view(cls, route):
		"""
		Define and return a function-based view depending on the route (provided as argument).
		"""
		def view(request, *args):
			# Instantiate class
			self = cls(route, request)

			# Return Response generated by handler
			return self.dispatch(request, *args)

		# Return ephemeral function-based view to URLconf
		return view

	def dispatch(self, request, *args):
		"""
		Dispatch to the right class method by looking up the route and HTTP method in the lookup table.
		"""
		method = request.method
		if '_method' in request.POST and request.POST['_method'].lower() in ['put', 'patch', 'delete']:
			method = request.POST['_method']

		try:
			handler = getattr(self, self.handler_method_names[self.route][method.lower()])
		except KeyError:
			# If route/method doesn't exist, return 405 Method Not Allowed with the allowed methods for current route
			allowed_methods = self.handler_method_names[self.route]
			return http.HttpResponseNotAllowed(allowed_methods)

		return handler(request, *args)

	def check_user(self, user):
		"""
		Compare the passed object to the current user and raise PermissionDenied if they are not equal.
		"""
		if user != self.request.user:
			raise PermissionDenied

	# Handler methods, must be overridden in child class

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
