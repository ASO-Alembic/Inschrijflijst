from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from lib.ResourceView import ResourceView, bind_model
from app.models import Committee


class CommitteeView(LoginRequiredMixin, ResourceView):
	models = [Committee]

	def index(self, request):
		# Get all committees for which the user is chairman
		committees = request.user.get_admined_committees()

		return render(request, 'committee_list.html', {'committees': committees})

	@bind_model
	def show(self, request, committee):
		request.user.check_admin_of(committee)

		return render(request, 'committee_detail.html', {'committee': committee})
