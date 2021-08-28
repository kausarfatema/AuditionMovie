from django.db import models
from django.utils import timezone
# Create your models here.
from accounts.models import Recruter, Talent, User, Category
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from .validators import file_size


class Ad(models.Model):
	name=models.CharField(max_length=100)
	recruter=models.ForeignKey(Recruter,on_delete=models.CASCADE)
	category=models.ForeignKey(Category,on_delete=models.CASCADE)
	talents=models.ManyToManyField(Talent,through='Application')
	date=models.DateField(default=None)
	img=models.ImageField(null=True,upload_to='ads',default='thumb_photos.png')
	apply_date=models.DateField(default=timezone.now)
	start_application = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	@property
	def is_past_due(self):
		return date.today() > self.date
	@property
	def is_not_the_time(self):
		return date.today() < self.apply_date

	@property
	def is_cannot_add(self):
		return date.today() < self.apply_date


class Application(models.Model):


	STATUS_CHOICES = [
		('Accepted','Accepted'),
		('Rejected','Rejected'),
		('Hold','Hold'),
		('Not Decided','Not Decided')
	]

	name=models.CharField(max_length=100)
	talent=models.ForeignKey(Talent, on_delete=models.CASCADE,null=True)
	ads=models.ForeignKey(Ad, on_delete=models.CASCADE)
	video=models.FileField(upload_to="videos/",null=True,validators=[file_size])
	application_status = models.CharField(max_length=40, choices= STATUS_CHOICES, default='Not Decided')
	thumbnail=models.ImageField(upload_to="thumbnails/",null=True, default='thumb_photos.png')
	recruter = models.ForeignKey(Recruter, models.CASCADE, null=True)
	
	
	class Meta:
		unique_together=[['talent','ads']]


class ApplPictures(models.Model):
	img=models.ImageField(null=True,upload_to='applpictures',default='thumb_photos.png')
	appli = models.ForeignKey(Application, on_delete=models.CASCADE)








