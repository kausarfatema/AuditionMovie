from django.db import models
from accounts.models import Photographer, Talent, Appointment
# Create your models here.

class Payment(models.Model):
	photographer=models.ForeignKey(Photographer,on_delete=models.CASCADE)
	talent=models.ForeignKey(Talent,on_delete=models.CASCADE)
	appointment=models.OneToOneField(Appointment,on_delete=models.CASCADE)
	txt_ref = models.CharField(max_length=900, null=True)
	status = models.CharField(max_length=800, null=True)
	transaction_id = models.CharField(max_length=900,null=True)
	ammount = models.IntegerField(default=0)


# Create your models here.
