from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from applications.models import PhotographerApplication
from accounts.models import RecruterApp

@shared_task
def sleepy(duration):
	sleep(duration)
	return None

@shared_task
def send_email_task(subject,message,fromMail,toArr):
	send_mail(subject,message,fromMail,toArr)
	return None

@shared_task
def delphoto(app_id):
	for id in app_id:
		application = PhotographerApplication.objects.get(pk=id)
		send_mail(
			'Photographer application',
			'your application has been rejected',
			'kausarbhimani7@gmail.com',
			[application.email],
			fail_silently=False,
		)
		application.delete()
	return None

@shared_task
def delrecruter(app_id):
	for id in app_id:
		application = RecruterApp.objects.get(pk=id)
		send_mail(
			'Photographer application',
			'your application has been rejected',
			'kausarbhimani7@gmail.com',
			[application.email],
			fail_silently=False,
		)
		application.delete()