from django.db import models


# Create your models here.

class PhotographerApplication(models.Model):
    app_choices = [ 
    ("1","Month"),
    ("2","Year"),
    ]
    type_work = [
        ("FR","Freelance"),
        ("CP","Company"),
    ]


    first_name=models.CharField(max_length=40)
    last_name=models.CharField(max_length=40)
    email=models.EmailField(max_length = 254,unique=True)
    name_of_photography_school=models.CharField(max_length=500)
    experience=models.IntegerField()
    experience_in_month_or_year= models.CharField(max_length=1,choices=app_choices)
    Type_of_Work = models.CharField(max_length=2,choices=type_work)
    is_rejected=models.BooleanField(default=True)
    is_employed=models.BooleanField(default=False)
    

    def __str__(self):
        return self.first_name