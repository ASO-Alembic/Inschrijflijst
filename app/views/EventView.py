from django.views.generic import ListView
from app.models import Event
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class EventListView(ListView):
	model = Event
