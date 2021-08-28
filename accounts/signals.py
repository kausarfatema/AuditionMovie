from django.dispatch import Signal
from .models import User
from django.dispatch import receiver
from .models import Recruter, Talent, Photographer
from django.db.models.signals import post_save

# Sent after a user successfully authenticates via a social provider,
# but before the login is actually processed. This signal is emitted
# for social logins, signups and when connecting additional social
# accounts to an account.
# Provides the arguments "request", "sociallogin"
pre_social_login = Signal()

# Sent after a user connects a social account to a their local account.
# Provides the arguments "request", "sociallogin"
social_account_added = Signal()

# Sent after a user connects an already existing social account to a
# their local account. The social account will have an updated token and
# refreshed extra_data.
# Provides the arguments "request", "sociallogin"
social_account_updated = Signal()

# Sent after a user disconnects a social account from their local
# account.
# Provides the arguments "request", "socialaccount"
social_account_removed = Signal()


@receiver(post_save,sender=User)
def create_profiles(sender,instance,created,**kwargs):
	if created:
		if instance.type_in_choices =='RC':
			Recruter.objects.create(user=instance)
		if instance.type_in_choices=='TL':
			Talent.objects.create(user=instance)

		if instance.type_in_choices=='PH':
			Photographer.objects.create(user=instance)



@receiver(post_save,sender=User)
def save_profiles(sender,instance,**kwargs):
	if instance.type_in_choices =='RC':
		instance.recruter.save()

	if instance.type_in_choices =='TL':
		instance.talent.save()

	if instance.type_in_choices=='PH':
		instance.photographer.save()