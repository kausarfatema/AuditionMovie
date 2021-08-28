from allauth.account.utils import perform_login
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import User
from . import signals
from django.conf import settings
from django.http import HttpResponseRedirect
from .socialmodel import SocialLogin
class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin): 
        user = sociallogin.user
        if user.id:  
            return          
        try:
            customer = User.objects.get(email=user.email)
            sociallogin.connect(request, customer)
            signals.social_account_added.send(
            sender=SocialLogin, request=request, sociallogin=sociallogin

        )
            return HttpResponseRedirect("/")
        except User.DoesNotExist:
            pass