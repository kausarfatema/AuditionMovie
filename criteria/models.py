from django.db import models
from ads.models import Ad
from accounts.models import Talent
# Create your models here.
from datetime import date   


class CriteriaQuestions(models.Model):
    ad =models.ForeignKey(Ad, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200) 
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

    def cannot_update(self):
        return date.today() > self.ad.apply_date

class Result(models.Model):
    STATUS_CHOICES = [
        ('F','FAIL'),
        ('P','PASS'),
    ]

    status = models.CharField(max_length=1, choices = STATUS_CHOICES, default= 'F' )
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()

class SavedResult(models.Model):
    question = models.CharField(max_length=600)
    answer = models.CharField(max_length=200)
    actual_answer =  models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    talent = models.ForeignKey(Talent, on_delete = models.CASCADE)   





