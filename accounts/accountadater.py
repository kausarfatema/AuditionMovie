from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect
from django.urls import reverse
class NoNewUsersAccountAdapter(DefaultAccountAdapter):

	def is_auto_signup_allowed(self, request,sociallogin):
		
		return False

	def get_login_redirect_url(self, request):
		if request.user.is_staff:
			return reverse("admin-panel")
		else:
			if request.user.type_in_choices == "TL":
				return reverse("filter-ad")

			elif request.user.type_in_choices =="RC":
				return reverse("recruter-dash")
			
			else:
				return reverse("photoappoint")