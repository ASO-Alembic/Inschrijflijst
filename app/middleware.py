from app.models import User


def proxy_user_middleware(get_response):
	"""
	Swap request.user with Proxy user class
	"""
	def middleware(request):
		if hasattr(request, 'user') and request.user.is_authenticated():
			request.user.__class__ = User

		response = get_response(request)
		return response
	return middleware
