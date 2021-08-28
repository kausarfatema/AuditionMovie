from django.contrib import admin
from .models import CriteriaQuestions, Result, SavedResult
# Register your models here.
admin.site.register(CriteriaQuestions)
admin.site.register(Result)
admin.site.register(SavedResult)