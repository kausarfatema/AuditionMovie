from django.db import models
from criteria.models import Criteria
# Create your models here.
class Question(models.Model):
    text = model.CharField(max_length=200)
    quiz = models.ForeignKey(Criteria, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.text)

    def get_answers(self):
        pass

def Answer(models.Model):
    text = models.CharField(max_length=200)
    correct=models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"question":self.question.text
