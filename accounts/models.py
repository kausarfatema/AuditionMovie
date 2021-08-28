from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from applications.models import PhotographerApplication
# Create your models here.
class Province(models.Model):
	name=models.CharField(max_length=100)
	def __str__(self):
		return self.name;

class District(models.Model):
	name=models.CharField(max_length=100)
	province=models.ForeignKey(Province,on_delete=models.CASCADE)
	def __str__(self):
		return self.name;


class Sector(models.Model):
	name =models.CharField(max_length=100)
	district=models.ForeignKey(District, on_delete=models.CASCADE)

	def __str__(self):
		return self.name;



class User(AbstractUser):
	
	RECRUTER='RC'
	TALENT='TL'
	PHOTOGRAPHER='PH'
	UNKNOWN='UN'
	TYPE_IN_CHOICES=[
		(RECRUTER,'Recruter'),
		(TALENT,'Talent'),
		(PHOTOGRAPHER,'Photographer'),
		(UNKNOWN,'Unknown'),

	]
	gender_list = (
		('Female','Female'),
		('Male', 'Male'),
	)
	type_in_choices=models.CharField(
		max_length=2,
		choices=TYPE_IN_CHOICES,
		default=UNKNOWN,
		)
	province=models.ForeignKey(Province,on_delete=models.CASCADE,null=True)
	district=models.ForeignKey(District,on_delete=models.CASCADE,null=True)
	sector=models.ForeignKey(Sector,on_delete=models.CASCADE,null=True)
	gender = models.CharField(max_length=10,choices=gender_list,default="Male")



class Category(models.Model):
	name=models.CharField(max_length=100)
	img=models.ImageField(null=True,upload_to='cat',default='thumb_photos.png')
	
	def __str__(self):
		return self.name


class RecruterApp(models.Model):
	gender_list = (
		('Female','Female'),
		('Male', 'Male'),
	)
	first_name = models.CharField(max_length = 60)
	lasT_name = models.CharField(max_length = 70)
	company_name = models.CharField(max_length=100,null=True)
	company_address = models.CharField(max_length=100,null=True)
	tin_number = models.CharField(max_length = 20,null=True)
	email = models.CharField(max_length = 90)
	is_rejected = models.BooleanField(default = False)
	is_employed =  models.BooleanField(default = False)
	province=models.ForeignKey(Province,on_delete=models.CASCADE,null=True)
	district=models.ForeignKey(District,on_delete=models.CASCADE,null=True)
	sector=models.ForeignKey(Sector,on_delete=models.CASCADE,null=True)
	gender = models.CharField(max_length=10,choices=gender_list,default="Male")

	def __str__(self):
		return self.company_name


class Recruter(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	company_name=models.CharField(max_length=100,null=True)
	company_address=models.CharField(max_length=100,null=True)
	originated_country=models.CharField(max_length=100,null=True)
	rec_application = models.OneToOneField(RecruterApp, on_delete=models.CASCADE, null=True)
	

	def __str__(self):
		return self.user.username + 'Recruter'


class Talent(models.Model):
	
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	category=models.ManyToManyField(Category,null=True)
	profile_picture=models.ImageField(upload_to='profile_picture',default='thumb_photos.png')

	def __str__(self):
		return self.user.username + 'Talent'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		SIZE = 300, 300
		if self.profile_picture:
			pic = Image.open(self.profile_picture.path)
			pic.thumbnail(SIZE, Image.LANCZOS)
			pic.save(self.profile_picture.path)

class Portfolio(models.Model):
	img = models.ImageField(null=True,upload_to='potfolio',default='thumb_photos.png')
	talent = models.ForeignKey(Talent, on_delete=models.CASCADE)

class Photographer(models.Model):
	talents=models.ManyToManyField(Talent,through='Appointment')
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	img=models.ImageField(null=True,upload_to='pho',default='thumb_photos.png')

	is_employed=models.BooleanField(default=False)
	application=models.OneToOneField(PhotographerApplication, on_delete=models.CASCADE, null=True)


	


class PhotoImage(models.Model):
	appl = models.ForeignKey(PhotographerApplication,on_delete=models.CASCADE, null=True)
	image=models.ImageField(upload_to='photographer_image')



class Appointment(models.Model):
	TIMESLOT_LIST = (
		('09:00 – 09:30', '09:00 – 09:30'),
		('10:00 – 10:30', '10:00 – 10:30'),
		('11:00 – 11:30', '11:00 – 11:30'),
		('12:00 – 12:30', '12:00 – 12:30'),
		('13:00 – 13:30', '13:00 – 13:30'),
		('14:00 – 14:30', '14:00 – 14:30'),
		('15:00 – 15:30', '15:00 – 15:30'),
		('16:00 – 16:30', '16:00 – 16:30'),
		('17:00 – 17:30', '17:00 – 17:30'),
	)
	SERVICES_LIST = (
		('Photoshooting','Photoshooting'),
		('videomaking', 'videomaking'),
	)
	A_STATUS = (
		('attended','attended'),
		('canceled', 'canceled'),
		('Not attended','Not attended'),
	)
	date = models.DateField(default=None, null=True)
	photographers=models.ForeignKey(Photographer,on_delete=models.CASCADE)
	talent=models.ForeignKey(Talent,on_delete=models.CASCADE)
	timeslot = models.CharField(choices=TIMESLOT_LIST,null=True, max_length=50)
	request_service = models.CharField(choices = SERVICES_LIST, default='videomaking',max_length= 255)
	status=models.BooleanField(default=False)
	att_status = models.CharField(choices=A_STATUS, max_length= 255, default= 'Not attended')

	class Meta:
		unique_together = ('photographers', 'date', 'timeslot')


class WorkFolder(models.Model):
	display_image = models.ImageField(upload_to='fold')
	name = models.CharField(max_length =360)
	photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)


class Photographerwork(models.Model):
	photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='work')
	fold = models.ForeignKey(WorkFolder, on_delete=models.CASCADE, null=True)


class Feedback(models.Model):
	photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
	talent=models.ForeignKey(Talent,on_delete=models.CASCADE,null=True)
	appointment = models.OneToOneField(Appointment,on_delete=models.CASCADE)
	description = models.TextField(null=True)


class CompanyBase(models.Model):
	company_name = models.CharField(max_length = 250)
	tin_number = models.CharField(max_length = 20)
	address = models.CharField(max_length =  300)
	owner_name = models.CharField(max_length= 60)

	def __str__(self):
		return self.company_name








# Create your models here.
