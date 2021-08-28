from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ad, Application


@receiver(post_save,sender=Ad)
def create_application(sender, instance, created, **kwargs):
	
	if created:
		Application.objects.create(ads=instance)
		print("Application created")


@receiver(post_save, sender=Ad)
def update_profile(sender, instance, created, **kwargs):
	if created == False:
		instance.application.save()
		print('profile updated')