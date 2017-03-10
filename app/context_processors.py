from django.utils import timezone


def now(request):
	return {'now': timezone.now()}


def base_url(request):
	return {'base_url': request.build_absolute_uri('/').strip("/")}
