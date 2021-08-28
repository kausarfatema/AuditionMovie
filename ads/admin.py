from django.contrib import admin
from .models import Ad, Application, ApplPictures
from accounts.models import Category
# Register your models here.
admin.site.register(Ad)

admin.site.register(Application)

admin.site.register(ApplPictures)
